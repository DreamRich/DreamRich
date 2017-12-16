from http import HTTPStatus
from dreamrich.tests_permissions import (
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser
)
from dreamrich.requests import RequestTypes
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)


class EmployeeToItself(UserToEmployee):

    factory_user = EmployeeMainFactory

    def test_employee_get_itself(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_employee_delete_itself(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_employee_put_itself(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_employee_patch_itself(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


class EmployeeToEmployee(UserToEmployee):

    factory_user = EmployeeMainFactory

    def setUp(self):
        self._initialize()
        self.consulted_instance = EmployeeMainFactory()

    def test_employee_get_employees_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.FORBIDDEN)

    def test_employee_get_employee(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.FORBIDDEN)

    def test_employee_post_employee(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.FORBIDDEN)

    def test_employee_delete_employee(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_employee_put_employee(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_employee_patch_employee(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


class EmployeeToClient(UserToClient):

    factory_user = EmployeeMainFactory

    def test_employee_get_clients_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.OK)

    def test_employee_get_client(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_employee_post_client(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.CREATED)

    def test_employee_delete_client(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_employee_put_client(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_employee_patch_client(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


class EmployeeToFinancialAdviser(UserToFinancialAdviser):

    factory_user = EmployeeMainFactory

    def test_employee_get_financial_advisers_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.FORBIDDEN)

    def test_employee_get_financial_adviser(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.FORBIDDEN)

    def test_employee_post_financial_adviser(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.FORBIDDEN)

    def test_employee_delete_financial_adviser(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_employee_put_financial_adviser(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_employee_patch_financial_adviser(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


class FinanicalAdviserToItself(UserToFinancialAdviser):

    factory_user = FinancialAdviserMainFactory

    def test_financial_adviser_get_itself(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_financial_adviser_delete_itself(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_itself(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_financial_adviser_patch_itself(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)


class FinanicalAdviserToFinanicalAdviser(UserToFinancialAdviser):

    factory_user = FinancialAdviserMainFactory

    def setUp(self):
        self._initialize()
        self.consulted_instance = FinancialAdviserMainFactory()

    def test_get_financial_advisers_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.OK)

    def test_financial_adviser_get_financial_adviser(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_financial_adviser_post_financial_adviser(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.CREATED)

    def test_financial_adviser_delete_financial_adviser(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_financial_adviser(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_financial_adviser_patch_financial_adviser(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)


# Tem que separar entre dele e de outros
class FinancialAdviserToClient(UserToClient):

    factory_user = FinancialAdviserMainFactory

    def test_financial_adviser_get_clients_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.OK)

    def test_financial_adviser_get_client(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_financial_adviser_post_client(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.CREATED)

    def test_financial_adviser_delete_client(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_client(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_financial_adviser_patch_client(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)


class FinancialAdviserToEmployee(UserToEmployee):

    factory_user = FinancialAdviserMainFactory

    def test_financial_adviser_get_employees_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.OK)

    def test_financial_adviser_get_employee(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_financial_adviser_post_employee(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.CREATED)

    def test_financial_adviser_delete_employee(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_employee(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_financial_adviser_patch_employee(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)
