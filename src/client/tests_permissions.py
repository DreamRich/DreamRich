from http import HTTPStatus
from dreamrich.tests_permissions import (
    UserToGeneral,
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser
)
from dreamrich.tests_permissions import Relationship
from dreamrich.requests import RequestTypes
from client.factories import ActiveClientMainFactory


class ClientToItself(UserToClient):

    factory_user = ActiveClientMainFactory

    def test_client_get_itself(self):
        self.user_test_request(RequestTypes.GET, HTTPStatus.OK)

    def test_client_delete_itself(self):
        self.user_test_request(RequestTypes.DELETE, HTTPStatus.FORBIDDEN)

    def test_client_put_itself(self):
        self.user_test_request(RequestTypes.PUT, HTTPStatus.OK)

    def test_client_patch_itself(self):
        self.user_test_request(RequestTypes.PATCH, HTTPStatus.OK)


class ClientToClient(UserToClient):

    factory_user = ActiveClientMainFactory

    def setUp(self):
        self._initialize()
        self.consulted = ActiveClientMainFactory()

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


class ClientToEmployee(UserToEmployee):

    factory_user = ActiveClientMainFactory

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


class ClientToFinancialAdviser(UserToFinancialAdviser):

    factory_user = ActiveClientMainFactory

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


class ClientToRelatedGeneral(UserToGeneral):

    factory_user = ActiveClientMainFactory

    consulted_relationship = Relationship(
        many=False,
        relationship_attr='active_client'
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


class ClientToGeneral(UserToGeneral):

    factory_user = ActiveClientMainFactory

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
