import json
from http import HTTPStatus
from collections import namedtuple
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
from .utils import authenticate_user


class PermissionsTests(TestCase):

    # For checking for instances which have relationship with user
    ConsultedRelationship = namedtuple('ConsultedRelationship',
                                       'many relationship_attr')

    # Children will fill these attributes
    factory_consulted = None
    factory_user = None
    serializer_consulted = None
    consulted = None
    django_client = None
    consulted_relationship = None
    base_route = ''

    def setUp(self):
        self._initialize()

    def user_test_request(self, method, status_code):

        # Test if user can make requests without being authenticated
        self.django_client = APIClient()
        response_status_code = self.make_request(method)
        self.assertEqual(response_status_code, HTTPStatus.UNAUTHORIZED)

        self.django_client = authenticate_user(self.user)
        response_status_code = self.make_request(method)
        self.assertEqual(response_status_code, status_code)

    def make_request(self, test_type, route=None):
        route = self._get_route(test_type) if not route else route

        http_method = self._handle_test_type(test_type)
        method = getattr(self.django_client, http_method)

        required_data_methods = [RequestTypes.PUT,
                                 RequestTypes.PATCH,
                                 RequestTypes.POST]

        # Prepare data and make request
        if test_type in required_data_methods:
            response = self._make_required_data_request(test_type,
                                                        method,
                                                        route)
        else:
            response = method(route)

        return response.status_code

    def _initialize(self):
        self.user = self.factory_user()  # pylint: disable=not-callable
        self.consulted = \
            self.factory_consulted()  # pylint: disable=not-callable

        if self.consulted_relationship:
            self._make_relationship(self.consulted, self.user)

    def _make_relationship(self, primary, secondary):
        # No problem at passing primary and secondary at reversed order
        many, attr = self.consulted_relationship  # pylint: disable=all

        # Primary will have primary key and secondary the foreign key
        if not hasattr(secondary, attr):
            primary, secondary = secondary, primary

            if not hasattr(secondary, attr):
                raise AttributeError('There is no relationship between'
                                     ' user and consulted classes')

        if many:
            attr = getattr(secondary, attr)
            attr.add(primary)  # Making relationship 1 or n to many
        else:
            secondary.delete()  # Avoid unique constraint problems
            setattr(secondary, attr, primary)  # Making relationship 1 to 1
            secondary.save()

    def _make_required_data_request(self, test_type, method, route):
        data = self.serializer_consulted(  # pylint: disable=not-callable
            self.consulted
        )
        data = data.data

        if test_type == RequestTypes.PATCH:  # Send data just to one field
            field = data.popitem()
            data = {field[0]: field[1]}
        elif test_type == RequestTypes.POST:  # Make a new one
            data.pop('pk')
            data['cpf'] = '75116625109'  # Generated online

        data = json.dumps(data)
        response = method(route, data, content_type='application/json')

        return response

    def _get_route(self, test_type):
        general_routes_tests = [RequestTypes.POST, RequestTypes.GETLIST]

        if test_type not in general_routes_tests:
            route = '{}{}/'.format(self.base_route, self.consulted.pk)
        else:
            route = self.base_route

        return route

    @staticmethod
    def _handle_test_type(test_type):
        if test_type not in RequestTypes:
            raise AttributeError('Invalid test type')

        # Handle test_types that are not http_methods
        if test_type == RequestTypes.GETLIST:
            http_method = RequestTypes.GET.value
        else:
            http_method = test_type.value

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
