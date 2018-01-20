from http import HTTPStatus
from dr_auth.tests_permissions import (
    UserToGeneral,
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser,
    UserToItself
)
from dr_auth.common_tests_permissions import (
    NotAuthenticatedTests,
    NotAuthenticatedToItselfTests
)
from dr_auth.tests_permissions import PermissionsTests
from dreamrich.requests import RequestTypes
from dreamrich.complete_factories import ActiveClientCompleteFactory


class ClientToItself(UserToClient,
                     UserToItself,
                     NotAuthenticatedToItselfTests):

    def test_client_get_itself(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_client_delete_itself(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_itself(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_client_patch_itself(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)


class ClientToClient(UserToClient,
                     PermissionsTests,
                     NotAuthenticatedTests):

    factory_user = ActiveClientCompleteFactory

    def test_client_get_clients_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.FORBIDDEN)

    def test_client_get_client(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.FORBIDDEN)

    def test_client_post_client(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.FORBIDDEN)

    def test_client_delete_client(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_client(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_client_patch_client(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


class ClientToEmployee(UserToEmployee,
                       PermissionsTests,
                       NotAuthenticatedTests):

    factory_user = ActiveClientCompleteFactory

    def test_clients_get_employees_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.FORBIDDEN)

    def test_client_get_employee(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.FORBIDDEN)

    def test_client_post_employee(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.FORBIDDEN)

    def test_client_delete_employee(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_employee(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_client_patch_employee(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


class ClientToFinancialAdviser(UserToFinancialAdviser,
                               PermissionsTests,
                               NotAuthenticatedTests):

    factory_user = ActiveClientCompleteFactory

    def test_clients_get_financial_advisers_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.FORBIDDEN)

    def test_client_get_financial_adviser(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.FORBIDDEN)

    def test_client_post_financial_adviser(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.FORBIDDEN)

    def test_client_delete_financial_adviser(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_financial_adviser(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_client_patch_financial_adviser(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)


class ClientToRelatedGeneral(UserToGeneral,
                             PermissionsTests,
                             NotAuthenticatedTests):

    factory_user = ActiveClientCompleteFactory

    relationship = PermissionsTests.Relationship(
        related_names='financial_planning',
        many=False
    )

    def test_client_get_generals_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.FORBIDDEN)

    def test_client_get_general(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_client_delete_general(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_general(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_client_patch_general(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)


class ClientToGeneral(UserToGeneral,
                      PermissionsTests,
                      NotAuthenticatedTests):

    factory_user = ActiveClientCompleteFactory

    def test_client_get_generals_list(self):
        self.user_test_request(RequestTypes.GETLIST, HTTPStatus.FORBIDDEN)

    def test_client_get_general(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.FORBIDDEN)

    def test_client_post_general(self):
        self.user_test_request(RequestTypes.POST, HTTPStatus.FORBIDDEN)

    def test_client_delete_general(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_general(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.FORBIDDEN)

    def test_client_patch_general(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.FORBIDDEN)
