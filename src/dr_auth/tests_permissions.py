import json
from http import HTTPStatus
from django.test import TestCase
from django.contrib.auth.models import Permission
from rest_framework.test import APIClient
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer
)
from employee.factories import EmployeeFactory, FinancialAdviserFactory
from client.factories import ActiveClientFactory
from client.serializers import ActiveClientSerializer
from financial_planning.serializers import FinancialPlanningSerializer
from financial_planning.factories import FinancialPlanningFactory
from dreamrich.requests import RequestTypes
from dreamrich.utils import Relationship
from .utils import authenticate_user


class PermissionsTests(TestCase):

    # Children will fill these attributes
    factory_consulted = None
    factory_user = None
    serializer_consulted = None
    django_client = None
    base_route = ''

    related_name = ''
    related_names = ('',)

    def setUp(self):
        # pylint: disable=not-callable
        self.user = self.factory_user()
        self.consulted = self.factory_consulted()
        # pylint: disable=not-callable

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

        required_data_methods = (RequestTypes.PUT,
                                 RequestTypes.PATCH,
                                 RequestTypes.POST)

        # Prepare data and make request
        if request_method in required_data_methods:
            response = self._make_required_data_request(request_method,
                                                        api_client_method,
                                                        route)
        else:
            response = api_client_method(route)

        return response.status_code

    def handle_related(self):
        if self.related_name:
            relationship = Relationship(
                self.user,
                related_name=self.related_name
            )
            self.consulted = relationship.get_related()
        elif self.related_names[0]:
            relationship = Relationship(
                self.user,
                related_name=self.related_names[0]
            )
            related_metas = tuple(
                Relationship.RelatedMeta(related_name, None)
                for related_name in self.related_names
            )
            self.consulted = relationship.get_nested_related(*related_metas)

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
        general_routes_tests = (RequestTypes.POST, RequestTypes.GETLIST)

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

        try:
            for field in read_only_fields:
                data.pop(field)
        except KeyError:
            pass

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


class UserToClient:

    factory_consulted = ActiveClientFactory
    serializer_consulted = ActiveClientSerializer
    base_route = '/api/client/active/'


class UserToEmployee:

    factory_consulted = EmployeeFactory
    serializer_consulted = EmployeeSerializer
    base_route = '/api/employee/employee/'


class UserToFinancialAdviser:

    factory_consulted = FinancialAdviserFactory
    serializer_consulted = FinancialAdviserSerializer
    base_route = '/api/employee/financial/'


# Refer to all others classes which have the same permissions
# Financial Planning was chosen for convenience
class UserToGeneral:

    factory_consulted = FinancialPlanningFactory
    serializer_consulted = FinancialPlanningSerializer
    base_route = '/api/financial_planning/financial_planning/'


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
