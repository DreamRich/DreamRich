import json
from http import HTTPStatus
from rest_framework.test import APIClient
from django.test import TestCase
from client.factories import ActiveClientMainFactory
from client.serializers import ActiveClientSerializer
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer
)
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)
from dreamrich.requests import RequestTypes
from .utils import authenticate_user


class PermissionsTests(TestCase):

    # Children will fill these variables
    factory_consulted = None
    factory_user = None
    serializer_consulted = None
    consulted_instance = None
    base_route = None
    django_client = None

    def setUp(self):
        self._initialize()

    def _initialize(self):
        self.user = self.factory_user()  # pylint: disable=not-callable
        self.consulted_instance = \
            self.factory_consulted()  # pylint: disable=not-callable

    def user_test_request(self, method, status_code):

        # Test if user can make requests without being authenticated
        self.django_client = APIClient()
        response_status_code = self.make_request(method)
        self.assertEqual(response_status_code, HTTPStatus.UNAUTHORIZED)

        self.django_client = authenticate_user(self.user)
        response_status_code = self.make_request(method)
        self.assertEqual(response_status_code, status_code)

    def make_request(self, test_type, route=None):
        require_data_methods = [RequestTypes.PUT,
                                RequestTypes.PATCH,
                                RequestTypes.POST]

        # Validate params
        if test_type not in RequestTypes:
            raise AttributeError('Invalid http method')

        # Handle test_types that are not http_methods
        if test_type == RequestTypes.GETLIST:
            http_method = RequestTypes.GET.value
        else:
            http_method = test_type.value

        method = getattr(self.django_client, http_method)
        route = self._get_route(test_type) if not route else route

        # Prepare data and make request
        if test_type in require_data_methods:
            data = self.serializer_consulted(  # pylint: disable=not-callable
                self.consulted_instance
            )
            data = data.data

            if test_type == RequestTypes.PATCH:  # Send data just to one field
                field = data.popitem()
                data = {field[0]: field[1]}
            elif test_type == RequestTypes.POST:  # Make a new one
                data.pop('id')
                data['cpf'] = '75116625109'  # Generated online

            data = json.dumps(data)

            response = method(route, data, content_type='application/json')
        else:
            response = method(route)

        return response.status_code

    def _get_route(self, test_type):
        general_routes_tests = [RequestTypes.POST, RequestTypes.GETLIST]

        if test_type not in general_routes_tests:
            route = '{}{}/'.format(self.base_route, self.consulted_instance.id)
        else:
            route = self.base_route

        return route


class UserToClient(PermissionsTests):

    factory_consulted = ActiveClientMainFactory
    serializer_consulted = ActiveClientSerializer
    base_route = '/api/client/active/'


class UserToEmployee(PermissionsTests):

    factory_consulted = EmployeeMainFactory
    serializer_consulted = EmployeeSerializer
    base_route = '/api/employee/employee/'


class UserToFinancialAdviser(PermissionsTests):

    factory_consulted = FinancialAdviserMainFactory
    serializer_consulted = FinancialAdviserSerializer
    base_route = '/api/employee/financial/'
