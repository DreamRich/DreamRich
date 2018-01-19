import json
from http import HTTPStatus
from collections import namedtuple
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import Permission
from dr_auth.serializers import BaseUserSerializer
from rest_framework_jwt.settings import api_settings
from dreamrich.requests import RequestTypes


def jwt_response_payload_handler(token, user=None, unused_request=None):
    context = BaseUserSerializer(user.baseuser).data
    context['token'] = token

    return context


def get_token(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)

    return token


def authenticate_user(user):
    django_client = APIClient()

    user_token = get_token(user)
    token = 'JWT {}'.format(user_token)

    django_client.credentials(HTTP_AUTHORIZATION=token)

    return django_client


class PermissionsTests(TestCase):

    # If nested relationship, just pass related_name like one.two.three,
    # many must be passed considering first and last on chain.
    Relationship = namedtuple('Relationship', 'related_names many')

    # Children will fill these attributes
    factory_consulted = None
    factory_user = None
    serializer_consulted = None
    django_client = None

    base_route = ''
    relationship = Relationship('', False)

    def setUp(self):
        # pylint: disable=not-callable
        self.user = self.factory_user()
        self.consulted = self.factory_consulted()

        self._check_attributes()
        self.handle_related()

    def user_test_request(self, request_method, status_code):
        self.django_client = authenticate_user(self.user)
        response_status_code = self.make_request(request_method)
        self.assertEqual(response_status_code, status_code)

    def user_test_not_authenticated_request(self, request_method):
        self.django_client = APIClient()
        response_status_code = self.make_request(request_method)
        self.assertEqual(response_status_code, HTTPStatus.UNAUTHORIZED)

    def make_request(self, request_method, route=None):
        route = self._get_route(request_method) if not route else route

        http_method = self._handle_request_method(request_method)
        api_client_method = getattr(self.django_client, http_method)

        required_data_methods = [RequestTypes.PUT,
                                 RequestTypes.PATCH,
                                 RequestTypes.POST]

        self._set_user_permissions()

        # Prepare data and make request
        if request_method in required_data_methods:
            response = self._make_required_data_request(request_method,
                                                        api_client_method,
                                                        route)
        else:
            response = api_client_method(route)

        return response.status_code

    def handle_related(self):
        if self.relationship.related_names:
            related_names = self.relationship.related_names
            user_name = self.user.__class__.__name__

            try:
                self.consulted = getattr(self.user, related_names)

            except AttributeError:
                raise AttributeError(
                    "'{}' passed to PermissionsTests.relationship"
                    " is not a valid related_names path or there is no created"
                    " object associated with {}.".format(related_names,
                                                         user_name)
                )

            if self.relationship.many:
                if self.consulted.last() is not None:
                    self.consulted = self.consulted.last()
                else:
                    raise AttributeError(
                        "There isn't any '{}' created and associated"
                        " with {}.".format(related_names, user_name)
                    )

    def _check_attributes(self):
        missing = ''

        if not self.consulted:
            missing = 'factory_consulted'
        elif not self.user:
            missing = 'factory_user'
        elif not self.serializer_consulted:
            missing = 'serializer_consulted'
        elif not self.base_route:
            missing = 'base_route'

        if missing:
            raise AttributeError('There are missing information in'
                                 ' permissions tests hierarchy,'
                                 ' {} is missing.'.format(missing))

    def _make_required_data_request(self, request_method,
                                    api_client_method, route):
        # pylint: disable=not-callable
        data_serialized = self.serializer_consulted(self.consulted)
        data = self._remove_read_only_fields(data_serialized)
        # pylint: enable=not-callable

        if request_method == RequestTypes.PATCH:
            field = data.popitem()
            data = {field[0]: field[1]}

        elif request_method == RequestTypes.POST:
            # When there was no use of "primary_key=True" on class definition
            # If the consulted has own primary key (pk isn't necessary)
            if hasattr(self.consulted, 'id'):
                try:
                    data.pop('pk')
                except KeyError:
                    pass

            self.consulted.delete()
            data['cpf'] = '75116625109'  # Arbitrary, generated online

        data = json.dumps(data)
        response = api_client_method(route, data,
                                     content_type='application/json')

        return response

    def _get_route(self, request_method):
        general_routes_tests = [RequestTypes.POST, RequestTypes.GETLIST]

        if request_method not in general_routes_tests:
            route = '{}{}/'.format(self.base_route, self.consulted.pk)
        else:
            route = self.base_route

        return route

    @staticmethod
    def _handle_request_method(request_method):
        if request_method not in RequestTypes:
            raise AttributeError('Invalid test type')

        # Handle request_methods that are not http_methods
        if request_method == RequestTypes.GETLIST:
            http_method = RequestTypes.GET.value
        else:
            http_method = request_method.value

        return http_method

    def _remove_read_only_fields(self, serialized_data):
        read_only_fields = self._get_read_only_fields(serialized_data)

        data = serialized_data.data
        for field in read_only_fields:
            data.pop(field)

        return data

    @staticmethod
    def _get_read_only_fields(data):
        all_fields = data.get_fields()
        all_fields_names = list(all_fields.keys())

        # Get all fields with read_only == True
        read_only_fields = \
            [name for name in all_fields_names if all_fields[name].read_only]

        # Remove id's fields
        read_only_fields = \
            [field for field in read_only_fields if field[-3:] != '_id']

        return read_only_fields

    # Permissions which are not being explicitly gotten from database inside
    # these tests are not being seen, probably because of database signals,
    # which are different at this environment. Fix when/if possible.
    def _set_user_permissions(self):
        for permission in self.user.default_permissions:
            fetched_permission = \
                Permission.objects.get(codename=permission.codename)
            self.user.user_permissions.add(fetched_permission)
