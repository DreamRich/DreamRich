from http import HTTPStatus
from dr_auth.permissions_tests_utils import (
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser,
    UserToGeneral,
    UserToItself,
    PermissionsTests
)
from dr_auth.common_tests_permissions import (
    NotAuthenticatedTests,
    NotAuthenticatedToItselfTests
)
from dreamrich.complete_factories import FinancialAdviserCompleteFactory
from .factories import (
    EmployeeFactory,
    FinancialAdviserFactory
)


class EmployeeToItself(UserToEmployee,
                       UserToItself,
                       NotAuthenticatedToItselfTests):

    def test_employee_retrieve_itself(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_employee_delete_itself(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_update_itself(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_employee_partial_update_itself(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class EmployeeToEmployee(UserToEmployee,
                         PermissionsTests,
                         NotAuthenticatedTests):

    factory_user = EmployeeFactory

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


class EmployeeToClient(UserToClient,
                       PermissionsTests,
                       NotAuthenticatedTests):

    factory_user = EmployeeFactory

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


class EmployeeToFinancialAdviser(UserToFinancialAdviser,
                                 PermissionsTests,
                                 NotAuthenticatedTests):

    factory_user = EmployeeFactory

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


class EmployeeToGeneral(UserToGeneral,
                        PermissionsTests,
                        NotAuthenticatedTests):

    factory_user = EmployeeFactory

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


class FinanicalAdviserToItself(UserToFinancialAdviser,
                               UserToItself,
                               NotAuthenticatedToItselfTests):

    def test_financial_adviser_retrieve_itself(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_delete_itself(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_update_itself(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_partial_update_itself(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinanicalAdviserToFinanicalAdviser(UserToFinancialAdviser,
                                         PermissionsTests,
                                         NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

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


class FinancialAdviserToRelatedClient(UserToClient,
                                      PermissionsTests,
                                      NotAuthenticatedTests):

    factory_user = FinancialAdviserCompleteFactory

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


class FinancialAdviserToClient(UserToClient,
                               PermissionsTests,
                               NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

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


class FinancialAdviserToEmployee(UserToEmployee,
                                 PermissionsTests,
                                 NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

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


class FinancialAdviserToRelatedGeneral(UserToGeneral,
                                       PermissionsTests,
                                       NotAuthenticatedTests):

    factory_user = FinancialAdviserCompleteFactory

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


class FinancialAdviserToGeneral(UserToGeneral,
                                PermissionsTests,
                                NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

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
