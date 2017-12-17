from http import HTTPStatus
from dreamrich.tests_permissions import UserToGeneral
from dreamrich.requests import RequestTypes
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)
from client.factories import ActiveClientMainFactory

# Here is general because these are tests for all models which have the same
# permissions. In other words, not users


# Tem que separar entre dele e de outros
class ClientToGeneral(UserToGeneral):

    factory_user = ActiveClientMainFactory

    def test_client_get_generals_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.OK)

    def test_client_get_general(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_client_post_general(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.CREATED)

    def test_client_delete_general(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_general(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_client_patch_general(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)


class EmployeeToGeneral(UserToGeneral):

    factory_user = EmployeeMainFactory

    def test_employee_get_general(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.FORBIDDEN)

    def test_employee_delete_general(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_employee_put_general(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_employee_patch_general(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


# tem que separar
class FinancialAdviserToGeneral(UserToGeneral):

    factory_user = FinancialAdviserMainFactory

    def test_financial_adviser_get_financial_advisers_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.OK)

    def test_financial_adviser_get_financial_adviser(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_financial_adviser_post_financial_adviser(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.CREATED)

    def test_financial_adviser_delete_financial_adviser(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_financial_adviser_put_financial_adviser(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_financial_adviser_patch_financial_adviser(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)
