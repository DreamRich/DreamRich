from django.test import TestCase
from client.factories import ActiveClientFactory
from django.contrib.auth.models import User
import ipdb
# Create your tests here.

class ClientUserTest(TestCase):
	def setUp(self):
		self.active_client = ActiveClientFactory()
		self.user = User.objects.last()

	def test_user_creation(self):
		self.assertIsNotNone(self.active_client.login)
		self.assertEqual(self.active_client.login.pk, self.user.pk)

	def test_username_client(self):
		self.assertEqual(self.active_client.cpf, self.user.username)

	def test_check_password(self):
		self.assertTrue(self.user.check_password('123456'))