import json
import employee.tests_permissions  # Can't do "from ..." because cyclic import
from django.test import TestCase
from dreamrich.utils import get_token
from rest_framework.test import APIClient
from client.factories import ActiveClientMainFactory


# Default user is client, but the class can be imported and other user used
# User is the one who will make the requests
class ToClient(TestCase):
    # Not special reasons on choices for routes, just ordinarys

    def setUp(self, user=None):
        self.django_client = APIClient()
        self.active_client = ActiveClientMainFactory()
        self.other_active_client = ActiveClientMainFactory()

        # Authenticate user
        self.token = 'JWT {}'.format(get_token(self.active_client))
        self.django_client.credentials(HTTP_AUTHORIZATION=self.token)

    @staticmethod
    def get_route(element=0, listing=False):
        route = '/api/client/'

        if listing:
            route = route
        elif element:
            route += 'address/{}/'.format(element)
        else:
            route += 'address/'

        return route

    def test_client_get_own_data(self):
        address_client_id = self.active_client.addresses.last().id

        route = self.get_route(address_client_id)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_client_put_own_data(self):
        client_id = self.active_client.pk
        state_id = self.active_client.addresses.last().state_id
        address_client_id = self.active_client.addresses.last().id

        route = self.get_route(address_client_id)

        response = self.django_client.put(
            route,
            json.dumps({
                'id': address_client_id,
                'city': 'Gama',
                'type_of_address': 'type0',
                'neighborhood': 'neighborhood0',
                'detail': 'detail0',
                'cep': '7000000',
                'number': 9965,
                'complement': 'complement0',
                'state_id': state_id,
                'active_client_id': client_id,
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)

    def test_client_patch_own_data(self):
        client_id = self.active_client.pk
        address_client_id = self.active_client.addresses.last().id
        state_id = self.active_client.addresses.last().state_id

        route = self.get_route(address_client_id)

        response = self.django_client.patch(
            route,
            json.dumps({
                'city': 'Gama',
                'state_id': state_id,
                'active_client_id': client_id,
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)

    def test_client_delete_own_data(self):
        address_client_id = self.active_client.addresses.last().id

        route = self.get_route(address_client_id)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 403)

    def test_user_get_client(self, status_code=403):
        other_client_address_id = self.other_active_client.addresses.last().id

        route = self.get_route(other_client_address_id)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, status_code)

    def test_user_put_client(self, status_code=403):
        other_client_id = self.other_active_client.pk
        other_state_id = self.other_active_client.addresses.last().state_id
        other_client_address_id = self.other_active_client.addresses.last().id

        route = self.get_route(other_client_address_id)

        response = self.django_client.put(
            route,
            json.dumps({
                'id': other_client_address_id,
                'city': 'Gama',
                'type_of_address': 'type0',
                'neighborhood': 'neighborhood0',
                'detail': 'detail0',
                'cep': '7000000',
                'number': 9965,
                'complement': 'complement0',
                'state_id': other_state_id,
                'active_client_id': other_client_id,
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)

    def test_user_patch_client(self, status_code=403):
        other_client_id = self.other_active_client.pk
        other_state_id = self.other_active_client.addresses.last().state_id
        other_client_address_id = self.other_active_client.addresses.last().id

        route = self.get_route(other_client_address_id)

        response = self.django_client.patch(
            route,
            json.dumps({
                'city': 'Gama',
                'state_id': other_state_id,
                'active_client_id': other_client_id,
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)

    def test_user_delete_client(self, status_code=403):
        address_client_id = self.active_client.addresses.last().id

        route = self.get_route(address_client_id)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, status_code)

    def test_clients_get_list(self, status_code=403):
        route = self.get_route(listing=True)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, status_code)

    def test_client_post(self, status_code=403):
        route = self.get_route()

        response = self.django_client.post(
            route,
            json.dumps({
                'city': 'asdf',
                'type_of_address': 'asdf',
                'neighborhood': 'This field is re',
                'detail': 'This field is required.',
                'cep': '71963000',
                'number': '8787',
                'complement': 'Ts required.',
                'state_id': '1',
                'active_client_id': str(self.active_client.pk)
            }),
            content_type='application/json')

        self.assertEqual(response.status_code, status_code)


class ClientToEmployee(TestCase):
    def setUp(self):
        self.active_client = ActiveClientMainFactory()

        self.employee_test = employee.tests_permissions \
                             .UserToEmployee()
        self.employee_test.setUp(self.active_client)

    def test_client_get_employee(self):
        self.employee_test.test_user_get_employee(status_code=403)

    def test_client_put_employee(self):
        self.employee_test.test_user_put_employee(status_code=403)

    def test_client_patch_employee(self):
        self.employee_test.test_user_patch_employee(status_code=403)

    def test_client_delete_employee(self):
        self.employee_test.test_user_delete_employee(status_code=403)

    def test_client_get_list(self):
        self.employee_test.test_get_employees_list(status_code=403)

    def test_client_post(self):
        self.employee_test.test_post_employee(status_code=403)


class ClientToFinancialAdviser(TestCase):
    def setUp(self):
        self.active_client = ActiveClientMainFactory()

        self.financial_adviser_test = employee.tests_permissions \
                                      .ToFinancialAdviser()

        self.financial_adviser_test.setUp(self.active_client)

    def test_client_get_financial_adviser(self):
        self.financial_adviser_test.test_user_get_financial_adviser(
            status_code=403
        )

    def test_client_put_financial_adviser(self):
        self.financial_adviser_test.test_user_put_financial_adviser(
            status_code=403
        )

    def test_client_patch_financial_adviser(self):
        self.financial_adviser_test.test_user_patch_financial_adviser(
            status_code=403
        )

    def test_client_delete_financial_adviser(self):
        self.financial_adviser_test.test_user_delete_financial_adviser(
            status_code=403
        )

    def test_client_get_list(self):
        self.financial_adviser_test.test_get_list_financial_advisers(
            status_code=403
        )

    def test_client_post(self):
        self.financial_adviser_test.test_post_financial_adviser(
            status_code=403
        )
