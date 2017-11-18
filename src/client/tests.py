from django.test import TestCase, Client as DjangoClient
from django.core.exceptions import ValidationError
from client.models import (
    ActiveClient,
    Client,
    BankAccount,
)
from client.factories import (
    ActiveClientMainFactory,
    ClientFactory,
)
import json


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
        self.django_client = DjangoClient()

        self.active_client = ActiveClientMainFactory()
        self.other_active_client = ActiveClientMainFactory()

    def test_client_own_data_get(self):
        address_client_id = self.active_client.addresses.last().id
        route = ('/api/client/address/' + str(address_client_id) + '/')
        response = self.django_client.get(route,
                                         {'username':
                                           self.active_client.username,
                                          'password': 'default123'})

        self.assertEqual(response.status_code, 200)

    def test_client_own_data_put(self):
        client_id = self.active_client.pk
        state_id = self.active_client.addresses.last().state_id
        address_client_id = self.active_client.addresses.last().id

        route = ('/api/client/address/' + str(address_client_id) + '/')

        response = self.django_client.put(
            route,
            json.dumps({
                'username': self.active_client.username,
                'password': 'default123',
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

        route = ('/api/client/address/' + str(address_client_id) + '/')

        response = self.django_client.patch(
            route,
            json.dumps({
                'username': self.active_client.username,
                'password': 'default123',
                'city': 'Gama',
                'state_id': state_id,
                'active_client_id': client_id,
             }),
             content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)

    def test_client_own_data_delete(self):
        address_client_id = self.active_client.addresses.last().id

        route = ('/api/client/address/' + str(address_client_id) + '/')

        response = self.django_client.get(route,
                                         {'username':
                                           self.active_client.username,
                                          'password': 'default123'})

        self.assertEqual(response.status_code, 403)
