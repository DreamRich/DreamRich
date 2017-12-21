from django.test import TestCase
from django.core.exceptions import ValidationError
from client.models import (
    ActiveClient, Address,
    Client, Country,
    BankAccount, State,
    Dependent,
)
from client.factories import (
    ActiveClientFactory,
    ClientFactory,
)


class ClientModelTest(TestCase):

    def setUp(self):
        self.active_client = ActiveClientFactory.build()
        self.client = ClientFactory.build()

    def test_save_active_client(self):
        self.active_client.save()
        self.assertEqual(ActiveClient.objects.last(), self.active_client)

    def test_save_client(self):
        self.client.save()
        self.assertEqual(Client.objects.last(), self.client)

    def test_save_active_client_with_cpf_right(self):
        self.active_client = ActiveClientFactory()
        active_client = ActiveClient.objects.last()
        active_client.cpf = "85726391012"
        active_client.save()
        self.assertEqual(ActiveClient.objects.last(), active_client)

    def test_not_save_active_client_with_cpf_wrong(self):
        self.active_client = ActiveClientFactory()
        active_client = ActiveClient.objects.last()
        active_client.cpf = "12345678901"
        with self.assertRaises(ValidationError):
            active_client.save()

    def test_save_active_client_with_phone_number_right(self):
        self.active_client = ActiveClientFactory()
        active_client = ActiveClient.objects.last()
        active_client.telephone = "(61) 9999-9999"
        active_client.save()
        self.assertEqual(ActiveClient.objects.last(), active_client)

    def test_not_save_active_client_with_phone_number_wrong(self):
        self.active_client = ActiveClientFactory()
        active_client = ActiveClient.objects.last()
        active_client.telephone = "9999-9999"
        with self.assertRaises(ValidationError):
            active_client.save()

    def test_save_active_client_with_agency_number_right(self):
        self.active_client = ActiveClientFactory()
        bank_account = BankAccount.objects.last()
        bank_account.agency = "1212-1"
        bank_account.save()
        self.assertEqual(BankAccount.objects.last(), bank_account)

    def test_not_save_active_client_with_agency_number_wrong(self):
        self.active_client = ActiveClientFactory()
        bank_account = BankAccount.objects.last()
        bank_account.agency = "12-1"
        with self.assertRaises(ValidationError):
            bank_account.save()

    def test_save_active_client_with_account_number_right(self):
        self.active_client = ActiveClientFactory()
        bank_account = BankAccount.objects.last()
        bank_account.account = "12121-1"
        bank_account.save()
        self.assertEqual(BankAccount.objects.last(), bank_account)

    def test_not_save_active_client_with_account_number_wrong(self):
        self.active_client = ActiveClientFactory()
        bank_account = BankAccount.objects.last()
        bank_account.account = "1212-1"
        with self.assertRaises(ValidationError):
            bank_account.save()

    def test_not_save_active_client_with_repeated_cpf(self):
        active_client = ActiveClientFactory()
        active_client = ActiveClient.objects.last()

        active_client2 = ActiveClientFactory()
        active_client2 = ActiveClient.objects.last()
        active_client2.cpf = active_client.cpf

        with self.assertRaises(ValidationError):
            active_client2.save()


class HistoricalClientCreateTest(TestCase):

    def _test_create_historic(self, model):
        self.assertEqual(model.history.count(), 0)
        ActiveClientFactory()
        self.assertEqual(model.history.count(), 1)

    def test_address(self):
        self._test_create_historic(Address)

    def test_active_client(self):
        self.assertEqual(ActiveClient.history.count(), 0)
        ActiveClientFactory()
        self.assertEqual(ActiveClient.history.count(), 2)

    def test_country(self):
        self._test_create_historic(Country)

    def test_bank_account(self):
        self._test_create_historic(BankAccount)

    def test_state(self):
        self._test_create_historic(State)

    def test_client(self):
        self._test_create_historic(Client)

    def test_dependent(self):
        self._test_create_historic(Dependent)
