from django.test import TestCase
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from client.models import (
		ActiveClient,
		Client,
)
from client.factories import (
		ActiveClientMainFactory,
		ClientFactory,
)
import pytest

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
		
		@pytest.mark.django_db
		def test_not_save_active_client(self):
				error_message = "Invalid CPF number."
				self.active_client = ActiveClientMainFactory()
				active_client = ActiveClient.objects.last()
				active_client.cpf = "12345678901"
				with self.assertRaises(ValidationError):
						active_client.save()
				
				
