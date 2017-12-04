import json
from django.test import TestCase
from django.core.exceptions import ValidationError
from dreamrich.utils import get_token
from rest_framework.test import APIClient
from client.models import (
    ActiveClient,
    Client,
    BankAccount,
)
from client.factories import (
    ActiveClientMainFactory,
    ClientFactory,
)


class ClientModelTest(TestCase):

    def setUp(self):
        self.active_client = ActiveClientMainFactory.build()
        self.client = ClientFactory.build()

    def test_save_active_client(self):
        self.active_client.save()
        self.assertEqual(ActiveClient.objects.last(), self.active_client)

    def test_save_client(self):
        self.client.save()
        self.assertEqual(Client.objects.last(), self.client)

    def test_save_active_client_with_cpf_right(self):
        self.active_client = ActiveClientMainFactory()
        active_client = ActiveClient.objects.last()
        active_client.cpf = "85726391012"
        active_client.save()
        self.assertEqual(ActiveClient.objects.last(), active_client)

    def test_not_save_active_client_with_cpf_wrong(self):
        self.active_client = ActiveClientMainFactory()
        active_client = ActiveClient.objects.last()
        active_client.cpf = "12345678901"
        with self.assertRaises(ValidationError):
            active_client.save()

    def test_save_active_client_with_phone_number_right(self):
        self.active_client = ActiveClientMainFactory()
        active_client = ActiveClient.objects.last()
        active_client.telephone = "(61) 9999-9999"
        active_client.save()
        self.assertEqual(ActiveClient.objects.last(), active_client)

    def test_not_save_active_client_with_phone_number_wrong(self):
        self.active_client = ActiveClientMainFactory()
        active_client = ActiveClient.objects.last()
        active_client.telephone = "9999-9999"
        with self.assertRaises(ValidationError):
            active_client.save()

    def test_save_active_client_with_agency_number_right(self):
        self.active_client = ActiveClientMainFactory()
        bank_account = BankAccount.objects.last()
        bank_account.agency = "1212-1"
        bank_account.save()
        self.assertEqual(BankAccount.objects.last(), bank_account)

    def test_not_save_active_client_with_agency_number_wrong(self):
        self.active_client = ActiveClientMainFactory()
        bank_account = BankAccount.objects.last()
        bank_account.agency = "12-1"
        with self.assertRaises(ValidationError):
            bank_account.save()

    def test_save_active_client_with_account_number_right(self):
        self.active_client = ActiveClientMainFactory()
        bank_account = BankAccount.objects.last()
        bank_account.account = "12121-1"
        bank_account.save()
        self.assertEqual(BankAccount.objects.last(), bank_account)

    def test_not_save_active_client_with_account_number_wrong(self):
        self.active_client = ActiveClientMainFactory()
        bank_account = BankAccount.objects.last()
        bank_account.account = "1212-1"
        with self.assertRaises(ValidationError):
            bank_account.save()

    def test_not_save_active_client_with_repeated_cpf(self):
        active_client = ActiveClientMainFactory()
        active_client = ActiveClient.objects.last()

        active_client2 = ActiveClientMainFactory()
        active_client2 = ActiveClient.objects.last()
        active_client2.cpf = active_client.cpf

        with self.assertRaises(ValidationError):
            active_client2.save()


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

    def test_client_own_data_get(self):
        address_client_id = self.active_client.addresses.last().id

        route = self._get_route(element=address_client_id)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_client_own_data_put(self):
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

    def test_client_own_data_patch(self):
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

    def test_client_own_data_delete(self):
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

    def test_client_get_list(self):
        route = self._get_route(listing=True)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 403)

    def test_client_post(self):
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
