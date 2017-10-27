from django.test import TestCase
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
