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

    def test_employee_get_itself(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_employee_delete_itself(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_put_itself(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_employee_patch_itself(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class EmployeeToEmployee(UserToEmployee,
                         PermissionsTests,
                         NotAuthenticatedTests):

    factory_user = EmployeeFactory

    def test_employee_get_employees_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_employee_get_employee(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_employee_post_employee(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_employee_delete_employee(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_put_employee(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_patch_employee(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class EmployeeToClient(UserToClient,
                       PermissionsTests,
                       NotAuthenticatedTests):

    factory_user = EmployeeFactory

    def test_employee_get_clients_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_employee_get_client(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_employee_post_client(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_employee_delete_client(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_put_client(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_patch_client(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class EmployeeToFinancialAdviser(UserToFinancialAdviser,
                                 PermissionsTests,
                                 NotAuthenticatedTests):

    factory_user = EmployeeFactory

    def test_employee_get_financial_advisers_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_employee_get_financial_adviser(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_employee_post_financial_adviser(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_employee_delete_financial_adviser(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_put_financial_adviser(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_patch_financial_adviser(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class EmployeeToGeneral(UserToGeneral,
                        PermissionsTests,
                        NotAuthenticatedTests):

    factory_user = EmployeeFactory

    def test_employee_get_general(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_employee_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_employee_put_general(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_employee_patch_general(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)

    def test_employee_post_general(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)


class FinanicalAdviserToItself(UserToFinancialAdviser,
                               UserToItself,
                               NotAuthenticatedToItselfTests):

    def test_financial_adviser_get_itself(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_delete_itself(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_itself(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_patch_itself(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinanicalAdviserToFinanicalAdviser(UserToFinancialAdviser,
                                         PermissionsTests,
                                         NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

    def test_get_financial_advisers_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_get_financial_adviser(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_post_financial_adviser(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_financial_adviser(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_financial_adviser(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_patch_financial_adviser(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinancialAdviserToRelatedClient(UserToClient,
                                      PermissionsTests,
                                      NotAuthenticatedTests):

    factory_user = FinancialAdviserCompleteFactory

    related_name = 'clients'

    def test_financial_adviser_get_clients_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_get_client(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_delete_client(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_client(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_patch_client(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinancialAdviserToClient(UserToClient,
                               PermissionsTests,
                               NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

    def test_financial_adviser_get_clients_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_get_client(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_post_client(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_client(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_put_client(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_patch_client(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class FinancialAdviserToEmployee(UserToEmployee,
                                 PermissionsTests,
                                 NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

    def test_financial_adviser_get_employees_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_get_employee(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_post_employee(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_employee(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_employee(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_patch_employee(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class FinancialAdviserToRelatedGeneral(UserToGeneral,
                                       PermissionsTests,
                                       NotAuthenticatedTests):

    factory_user = FinancialAdviserCompleteFactory

    related_names = ('clients', 'financial_planning')

    def test_financial_adviser_get_generals_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_get_general(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.NO_CONTENT)

    def test_financial_adviser_put_general(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_financial_adviser_patch_general(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class FinancialAdviserToGeneral(UserToGeneral,
                                PermissionsTests,
                                NotAuthenticatedTests):

    factory_user = FinancialAdviserFactory

    def test_financial_adviser_get_generals_list(self):
        self.user_test_request('list', HTTPStatus.OK)

    def test_financial_adviser_get_general(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_financial_adviser_post_general(self):
        self.user_test_request('create', HTTPStatus.CREATED)

    def test_financial_adviser_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_financial_adviser_put_general(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def financial_adviser_patch_general(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)
