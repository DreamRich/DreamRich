from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer
)
from employee.factories import (
    EmployeeFactory,
    FinancialAdviserFactory
)
from client.factories import ActiveClientFactory
from client.serializers import ActiveClientSerializer
from financial_planning.serializers import FinancialPlanningSerializer
from financial_planning.factories import FinancialPlanningFactory
from dreamrich.requests import RequestTypes
from .utils import PermissionsTests


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
