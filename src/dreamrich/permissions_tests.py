import json
from http import HTTPStatus
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import Permission
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer
)
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)
from client.factories import ActiveClientFactory
from client.serializers import ActiveClientSerializer
from financial_planning.factories import FinancialPlanningFactory
from financial_planning.serializers import FinancialPlanningSerializer
from .requests import RequestTypes
from .utils import authenticate_user, Relationship


class UserToClient:

    factory_consulted = ActiveClientFactory
    serializer_consulted = ActiveClientSerializer
    base_route = '/api/client/active/'


class UserToEmployee:

    factory_consulted = EmployeeMainFactory
    serializer_consulted = EmployeeSerializer
    base_route = '/api/employee/employee/'


class UserToFinancialAdviser:

    factory_consulted = FinancialAdviserMainFactory
    serializer_consulted = FinancialAdviserSerializer
    base_route = '/api/employee/financial/'


# Refer to all others classes which have the same permissions
# Financial Planning was chosen for convenience
class UserToGeneral:

    factory_consulted = FinancialPlanningFactory
    serializer_consulted = FinancialPlanningSerializer
    base_route = '/api/financial_planning/financial_planning/'


class NotAuthenticatedTests:
    # pylint: disable=not-callable

    user_test_not_authenticated_request = None  # pylint: disable=invalid-name

    def test_user_get_list_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.GETLIST)

    def test_user_get_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.GET)

    def test_user_post_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.POST)

    def test_user_delete_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.DELETE)

    def test_user_put_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PUT)

    def test_user_patch_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PATCH)


class NotAuthenticatedToItselfTests:
    # pylint: disable=not-callable

    user_test_not_authenticated_request = None  # pylint: disable=invalid-name

    def test_user_get_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.GET)

    def test_user_delete_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.DELETE)

    def test_user_put_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PUT)

    def test_user_patch_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PATCH)


class PermissionsTests(TestCase):

    # Children will fill these attributes
    factory_consulted = None
    factory_user = None
    serializer_consulted = None
    base_route = ''

    django_client = None

    def setUp(self):
        # pylint: disable=not-callable
        self._check_attributes()

        self.user = self.factory_user()
        self.consulted = self.factory_consulted()

        # Relationship will be made if call make() or pass all the data
        # Attribution just to set default value
        # Must be a list if more than one relationship is necessary (nested)
        self.consulted_relationships = Relationship(
            primary=self.user,
            secondary=self.consulted,
        )

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

    def _check_attributes(self):
        missing = ''

        if not self.factory_consulted:
            missing = 'factory_consulted'
        elif not self.factory_user:
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

        # Remove id fields
        read_only_fields = \
            [field for field in read_only_fields if field[-3:] != '_id']

        return read_only_fields

    # Permissions not explicitly gotten from database inside these tests are
    # not being seen. Probably because of database signals which are different
    # at this environment. Fix when/if possible
    def _set_user_permissions(self):
        for permission in self.user.default_permissions:
            fetched_permission = \
                Permission.objects.get(codename=permission.codename)
            self.user.user_permissions.add(fetched_permission)


class UserToItself(PermissionsTests):

    def setUp(self):
        # pylint: disable=not-callable
        self.consulted = self.factory_consulted()
        self.user = self.consulted

    def _check_attributes(self):
        missing = ''

        if not self.factory_consulted:
            missing = 'factory_consulted'
        elif not self.serializer_consulted:
            missing = 'serializer_consulted'
        elif not self.base_route:
            missing = 'base_route'

        if missing:
            raise AttributeError('There are missing information in'
                                 ' permissions tests hierarchy,'
                                 ' {} is missing.'.format(missing))
