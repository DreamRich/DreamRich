from http import HTTPStatus
from dr_auth.permissions_tests_utils import (
    ClientToModel,
    UserToGeneral,
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser,
)
from dr_auth.common_tests_permissions import (
    NotAuthenticatedTests,
    NotAuthenticatedToItselfTests
)
from dr_auth.permissions_tests_utils import PermissionsTests


class ClientToItself(ClientToModel, UserToClient, PermissionsTests,
                     NotAuthenticatedToItselfTests):

    to_itself = True

    def test_client_retrieve_itself(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_client_delete_itself(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_client_update_itself(self):
        self.user_test_request('update', HTTPStatus.OK)

    def test_client_partial_update_itself(self):
        self.user_test_request('partial_update', HTTPStatus.OK)


class ClientToClient(ClientToModel, UserToClient, PermissionsTests,
                     NotAuthenticatedTests):

    def test_client_retrieve_clients_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_client_retrieve_client(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_client_create_client(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_client_delete_client(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_client_update_client(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_client_partial_update_client(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class ClientToEmployee(ClientToModel, UserToEmployee, PermissionsTests,
                       NotAuthenticatedTests):

    def test_clients_retrieve_employees_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_client_retrieve_employee(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_client_create_employee(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_client_delete_employee(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_client_update_employee(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_client_partial_update_employee(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class ClientToFinancialAdviser(ClientToModel, UserToFinancialAdviser,
                               PermissionsTests, NotAuthenticatedTests):

    def test_clients_retrieve_financial_advisers_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_client_retrieve_financial_adviser(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_client_create_financial_adviser(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_client_delete_financial_adviser(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_client_update_financial_adviser(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_client_partial_update_financial_adviser(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class ClientToRelatedGeneral(ClientToModel, UserToGeneral, PermissionsTests,
                             NotAuthenticatedTests):

    related_name = 'financial_planning'

    def test_client_retrieve_generals_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_client_retrieve_general(self):
        self.user_test_request('retrieve', HTTPStatus.OK)

    def test_client_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_client_update_general(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_client_partial_update_general(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)


class ClientToGeneral(ClientToModel, UserToGeneral, PermissionsTests,
                      NotAuthenticatedTests):

    def test_client_retrieve_generals_list(self):
        self.user_test_request('list', HTTPStatus.FORBIDDEN)

    def test_client_retrieve_general(self):
        self.user_test_request('retrieve', HTTPStatus.FORBIDDEN)

    def test_client_create_general(self):
        self.user_test_request('create', HTTPStatus.FORBIDDEN)

    def test_client_delete_general(self):
        self.user_test_request('destroy', HTTPStatus.FORBIDDEN)

    def test_client_update_general(self):
        self.user_test_request('update', HTTPStatus.FORBIDDEN)

    def test_client_partial_update_general(self):
        self.user_test_request('partial_update', HTTPStatus.FORBIDDEN)
