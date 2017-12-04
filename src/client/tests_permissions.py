import json
from django.test import TestCase
from dreamrich.utils import get_token
from rest_framework.test import APIClient
from client.factories import ActiveClientMainFactory


class ClientPermissionsTest(TestCase):
    # Not special reasons on choices for routes, just ordinarys

    def setUp(self):
        self.django_client = APIClient()
        self.active_client = ActiveClientMainFactory()
        self.other_active_client = ActiveClientMainFactory()

        # Authenticate user
        self.token = 'JWT {}'.format(get_token(self.active_client))
        self.django_client.credentials(HTTP_AUTHORIZATION=self.token)

    @staticmethod
    def _get_route(element=0, listing=False):
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

        route = self._get_route(element=address_client_id)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_client_put_own_data(self):
        client_id = self.active_client.pk
        state_id = self.active_client.addresses.last().state_id
        address_client_id = self.active_client.addresses.last().id

        route = self._get_route(element=address_client_id)

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

        route = self._get_route(element=address_client_id)

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

        route = self._get_route(element=address_client_id)

        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 403)

    def test_get_other_client_data(self):
        other_client_address_id = self.other_active_client.addresses.last().id

        route = self._get_route(element=other_client_address_id)

        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 403)

    def test_put_other_client_data(self):
        other_client_id = self.other_active_client.pk
        other_state_id = self.other_active_client.addresses.last().state_id
        other_client_address_id = self.other_active_client.addresses.last().id

        route = '/api/client/address/' + str(other_client_address_id) + '/'

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

        self.assertEqual(response.status_code, 403)

    def test_patch_other_client_data(self):
        other_client_id = self.other_active_client.pk
        other_state_id = self.other_active_client.addresses.last().state_id
        other_client_address_id = self.other_active_client.addresses.last().id

        route = '/api/client/address/' + str(other_client_address_id) + '/'

        response = self.django_client.patch(
            route,
            json.dumps({
                'city': 'Gama',
                'state_id': other_state_id,
                'active_client_id': other_client_id,
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_other_client_data(self):
        address_client_id = self.active_client.addresses.last().id

        route = self._get_route(element=address_client_id)

        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 403)

    def test_get_list_clients(self):
        route = self._get_route(listing=True)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 403)

    def test_post_client(self):
        route = self._get_route()

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

        self.assertEqual(response.status_code, 403)
