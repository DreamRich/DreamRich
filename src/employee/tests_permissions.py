from http import HTTPStatus
from dr_auth.permissions_tests_utils import (
    EmployeeToModel,
    FinancialAdviserToModel,
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser,
    UserToGeneral,
    PermissionsTests
)
from dr_auth.common_tests_permissions import (
    NotAuthenticatedTests,
    NotAuthenticatedToItselfTests
)


class EmployeeToItself(EmployeeToModel, UserToEmployee, PermissionsTests,
                       NotAuthenticatedToItselfTests):

    to_itself = True

    def test_employee_retrieve_itself(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_employee_delete_itself(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_update_itself(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_employee_partial_update_itself(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class EmployeeToEmployee(EmployeeToModel, UserToEmployee, PermissionsTests,
                         NotAuthenticatedTests):

    def test_employee_retrieve_employees_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_employee_retrieve_employee(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_employee_create_employee(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_employee_delete_employee(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_update_employee(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_partial_update_employee(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class EmployeeToClient(EmployeeToModel, UserToClient, PermissionsTests,
                       NotAuthenticatedTests):

    def test_employee_retrieve_clients_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_employee_retrieve_client(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_employee_create_client(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_employee_delete_client(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_update_client(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_partial_update_client(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class EmployeeToFinancialAdviser(EmployeeToModel, UserToFinancialAdviser,
                                 PermissionsTests, NotAuthenticatedTests):

    def test_employee_retrieve_financial_advisers_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_employee_retrieve_financial_adviser(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_employee_create_financial_adviser(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_employee_delete_financial_adviser(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_update_financial_adviser(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_partial_update_financial_adviser(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class EmployeeToGeneral(EmployeeToModel, UserToGeneral, PermissionsTests,
                        NotAuthenticatedTests):

    def test_employee_retrieve_general(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_employee_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_update_general(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_partial_update_general(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)

    def test_employee_create_general(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)


class FinanicalAdviserToItself(FinancialAdviserToModel, UserToFinancialAdviser,
                               PermissionsTests,
                               NotAuthenticatedToItselfTests):

    def test_financial_adviser_retrieve_itself(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_delete_itself(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_update_itself(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_partial_update_itself(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinanicalAdviserToFinanicalAdviser(FinancialAdviserToModel,
                                         UserToFinancialAdviser,
                                         PermissionsTests,
                                         NotAuthenticatedTests):

    def test_retrieve_financial_advisers_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_retrieve_financial_adviser(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_create_financial_adviser(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_financial_adviser(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_update_financial_adviser(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_partial_update_financial_adviser(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinancialAdviserToRelatedClient(FinancialAdviserToModel, UserToClient,
                                      PermissionsTests, NotAuthenticatedTests):

    related_name = 'clients'

    def test_financial_adviser_retrieve_clients_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_retrieve_client(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_delete_client(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_update_client(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_partial_update_client(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinancialAdviserToClient(FinancialAdviserToModel, UserToClient,
                               PermissionsTests, NotAuthenticatedTests):

    def test_financial_adviser_retrieve_clients_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_retrieve_client(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_create_client(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_client(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_update_client(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_partial_update_client(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class FinancialAdviserToEmployee(FinancialAdviserToModel, UserToEmployee,
                                 PermissionsTests, NotAuthenticatedTests):

    def test_financial_adviser_retrieve_employees_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_retrieve_employee(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_create_employee(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_employee(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_update_employee(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_partial_update_employee(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class FinancialAdviserToRelatedGeneral(FinancialAdviserToModel, UserToGeneral,
                                       PermissionsTests,
                                       NotAuthenticatedTests):

    related_names = ('clients', 'financial_planning')

    def test_financial_adviser_retrieve_generals_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_retrieve_general(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_update_general(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_partial_update_general(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinancialAdviserToGeneral(FinancialAdviserToModel, UserToGeneral,
                                PermissionsTests, NotAuthenticatedTests):

    def test_financial_adviser_retrieve_generals_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_retrieve_general(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_create_general(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_update_general(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def financial_adviser_partial_update_general(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)
