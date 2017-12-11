from dreamrich.tests_permissions import (
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser
)
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)


class EmployeeToItself(UserToEmployee):

    factory_user = EmployeeMainFactory

    def test_employee_get_itself(self):
        self.user_get_request(200)

    def test_employee_delete_itself(self):
        self.user_delete_request(403)

    def test_employee_put_itself(self):
        self.user_put_request(403)

    def test_employee_patch_itself(self):
        self.user_patch_request(403)


class EmployeeToEmployee(UserToEmployee):

    factory_user = EmployeeMainFactory

    def setUp(self):
        self._initialize()
        self.consulted_instance = EmployeeMainFactory()

    def test_employee_get_employees_list(self):
        self.user_get_list_request(403)

    def test_employee_get_employee(self):
        self.user_get_request(403)

    def test_employee_post_employee(self):
        self.user_post_request(403)

    def test_employee_delete_employee(self):
        self.user_delete_request(403)

    def test_employee_put_employee(self):
        self.user_put_request(403)

    def test_employee_patch_employee(self):
        self.user_patch_request(403)


class EmployeeToClient(UserToClient):

    factory_user = EmployeeMainFactory

    def test_employee_get_clients_list(self):
        self.user_get_list_request(200)

    def test_employee_get_client(self):
        self.user_get_request(200)

    def test_employee_post_client(self):
        self.user_post_request(201)

    def test_employee_delete_client(self):
        self.user_delete_request(204)

    def test_employee_put_client(self):
        self.user_put_request(200)

    def test_employee_patch_client(self):
        self.user_patch_request(200)


class EmployeeToFinancialAdviser(UserToFinancialAdviser):

    factory_user = EmployeeMainFactory

    def test_employee_get_financial_advisers_list(self):
        self.user_get_list_request(403)

    def test_employee_get_financial_adviser(self):
        self.user_get_request(403)

    def test_employee_post_financial_adviser(self):
        self.user_post_request(403)

    def test_employee_delete_financial_adviser(self):
        self.user_delete_request(403)

    def test_employee_put_financial_adviser(self):
        self.user_put_request(403)

    def test_employee_patch_financial_adviser(self):
        self.user_patch_request(403)


class FinanicalAdviserToItself(UserToFinancialAdviser):

    factory_user = FinancialAdviserMainFactory

    def test_financial_adviser_get_itself(self):
        self.user_get_request(200)

    def test_financial_adviser_delete_itself(self):
        self.user_delete_request(204)

    def test_financial_adviser_put_itself(self):
        self.user_put_request(200)

    def test_financial_adviser_patch_itself(self):
        self.user_patch_request(200)


class FinanicalAdviserToFinanicalAdviser(UserToFinancialAdviser):

    factory_user = FinancialAdviserMainFactory

    def setUp(self):
        self._initialize()
        self.consulted_instance = FinancialAdviserMainFactory()

    def test_get_financial_advisers_list(self):
        self.user_get_list_request(200)

    def test_financial_adviser_get_financial_adviser(self):
        self.user_get_request(200)

    def test_financial_adviser_post_financial_adviser(self):
        self.user_post_request(201)

    def test_financial_adviser_delete_financial_adviser(self):
        self.user_delete_request(204)

    def test_financial_adviser_put_financial_adviser(self):
        self.user_put_request(200)

    def test_financial_adviser_patch_financial_adviser(self):
        self.user_patch_request(200)


class FinancialAdviserToClient(UserToClient):

    factory_user = FinancialAdviserMainFactory

    def test_financial_adviser_get_clients_list(self):
        self.user_get_list_request(200)

    def test_financial_adviser_get_client(self):
        self.user_get_request(200)

    def test_financial_adviser_post_client(self):
        self.user_post_request(201)

    def test_financial_adviser_delete_client(self):
        self.user_delete_request(204)

    def test_financial_adviser_put_client(self):
        self.user_put_request(200)

    def test_financial_adviser_patch_client(self):
        self.user_patch_request(200)


class FinancialAdviserToEmployee(UserToEmployee):

    factory_user = FinancialAdviserMainFactory

    def test_financial_adviser_get_employees_list(self):
        self.user_get_list_request(200)

    def test_financial_adviser_get_employee(self):
        self.user_get_request(200)

    def test_financial_adviser_post_employee(self):
        self.user_post_request(201)

    def test_financial_adviser_delete_employee(self):
        self.user_delete_request(204)

    def test_financial_adviser_put_employee(self):
        self.user_put_request(200)

    def test_financial_adviser_patch_employee(self):
        self.user_patch_request(200)
