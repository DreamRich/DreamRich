import json
from http import HTTPStatus
from rest_framework.test import APIClient
from django.test import TestCase
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer
)
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)
from client.factories import ActiveClientMainFactory
from client.serializers import ActiveClientSerializer
from financial_planning.factories import FinancialPlanningFactory
from financial_planning.serializers import FinancialPlanningSerializer
from .requests import RequestTypes
from .utils import authenticate_user, Relationship


class PermissionsTests(TestCase):

    # Children will fill these attributes
    factory_consulted = None
    factory_user = None
    serializer_consulted = None
    django_client = None
    base_route = ''

    def setUp(self):
        self.user = self.factory_user()  # pylint: disable=not-callable
        self.consulted = \
            self.factory_consulted()  # pylint: disable=not-callable

        # Relationship will be made if call make() or pass all the data
        # Attribution just to set default value
        # Can be a list if more than one relationship is necessary (nested)
        self.consulted_relationships = Relationship(
            primary=self.user,
            secondary=self.consulted,
        )

    def user_test_request(self, request_method, status_code):

        # Test if user can make requests without being authenticated
        self.django_client = APIClient()
        response_status_code = self.make_request(request_method)
        self.assertEqual(response_status_code, HTTPStatus.UNAUTHORIZED)

        self.django_client = authenticate_user(self.user)
        response_status_code = self.make_request(request_method,
                                                 is_authenticated=True)
        self.assertEqual(response_status_code, status_code)

    def make_request(self, request_method, route=None, is_authenticated=False):
        route = self._get_route(request_method) if not route else route

        http_method = self._handle_request_method(request_method)
        api_client_method = getattr(self.django_client, http_method)

        required_data_methods = [RequestTypes.PUT,
                                 RequestTypes.PATCH,
                                 RequestTypes.POST]

        # Prepare data and make request
        if request_method in required_data_methods:
            response = self._make_required_data_request(request_method,
                                                        api_client_method,
                                                        route,
                                                        is_authenticated)
        else:
            response = api_client_method(route)

        return response.status_code

    def _make_required_data_request(self, request_method,
                                    api_client_method, route,
                                    is_authenticated):
        data = self.serializer_consulted(  # pylint: disable=not-callable
            self.consulted
        )
        data = data.data

        if request_method == RequestTypes.PATCH:  # Send data just to one field
            field = data.popitem()
            data = {field[0]: field[1]}
        elif request_method == RequestTypes.POST:  # Make a new one
            # The consulted has own primary key and the pk isn't necessary
            if hasattr(self.consulted, 'id'):
                data.pop('pk')
            if is_authenticated:
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


# Refer to all others classes which have the same permissions
class UserToGeneral(PermissionsTests):

    factory_consulted = FinancialPlanningFactory
    serializer_consulted = FinancialPlanningSerializer
    base_route = '/api/financial_planning/financial_planning/'
