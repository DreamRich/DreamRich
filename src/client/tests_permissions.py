from dreamrich.tests_permissions import (
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser
)
from client.factories import ActiveClientMainFactory


class ClientToItself(UserToClient):

    def test_client_get_itself(self):
        self.user_get_request(200)

    def test_client_delete_itself(self):
        self.user_delete_request(403)

    def test_client_put_itself(self):
        self.user_put_request(403)

    def test_client_patch_itself(self):
        self.user_patch_request(403)


class ClientToClient(UserToClient):

    def setUp(self):
        self._initialize()
        self.consulted_instance = ActiveClientMainFactory().id

    def test_client_get_clients_list(self):
        self.user_get_list_request(403)

    def test_client_get_client(self):
        self.user_get_request(403)

    def test_client_post(self):
        self.user_post_request(403)

    def test_client_delete_client(self):
        self.user_delete_request(403)

    def test_client_put_client(self):
        self.user_put_request(403)

    def test_client_patch_client(self):
        self.user_patch_request(403)


class ClientToEmployee(UserToEmployee):

    def test_clients_get_employees_list(self):
        self.user_get_list_request(200)

    def test_client_get_employee(self):
        self.user_get_request(200)

    def test_client_post(self):
        self.user_post_request(201)

    def test_client_delete_employee(self):
        self.user_delete_request(204)

    def test_client_put_employee(self):
        self.user_put_request(200)

    def test_client_patch_employee(self):
        self.user_patch_request(200)


class ClientToFinancialAdviser(UserToFinancialAdviser):

    def test_clients_get_financial_advisers_list(self):
        self.user_get_list_request(200)

    def test_client_get_financial_adviser(self):
        self.user_get_request(200)

    def test_client_post(self):
        self.user_post_request(201)

    def test_client_delete_financial_adviser(self):
        self.user_delete_request(204)

    def test_client_put_financial_adviser(self):
        self.user_put_request(200)

    def test_client_patch_financial_adviser(self):
        self.user_patch_request(200)
