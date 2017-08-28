from django.test import TestCase, Client
from dr_auth.factories import UserFactory
from client.factories import ActiveClientMainFactory
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from json import dumps


class AuthTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client = Client()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

    def test_get_token(self):
        response = self.client.post('/api/auth/',
                                    {'username': self.user.username,
                                     'password': 'def123'})
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data['token'] is not None)
        self.assertEqual(response.data['roles'], {'is_adm': True})

    def test_not_get_token(self):
        response = self.client.post('/api/auth/',
                                    {'username': self.user.username,
                                     'password': 'DEFAULT123'})
        self.assertEqual(response.status_code, 400)


class PasswordChange(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client = Client()

    def test_user_change_password(self):
        response = self.client.post('/api/auth/password/',
                                    {'userid': self.user.pk,
                                     'password': 'def123',
                                     'new_password': 'DEFAULT123',
                                     'new_password_confirmation': 'DEFAULT123',
                                     })

        self.assertEqual(response.data, dumps({'detail': 'password changed'}))

    def test_user_match_change_password(self):
        self.client.post('/api/auth/password/',
                         {'userid': self.user.pk,
                          'password': 'def123',
                          'new_password': 'DEFAULT123',
                          'new_password_confirmation': 'DEFAULT123',
                          })
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password('DEFAULT123'))

    def test_different_passwords(self):
        response = self.client.post('/api/auth/password/',
                                    {'userid': self.user.pk,
                                     'password': 'def123',
                                     'new_password': 'default123',
                                     'new_password_confirmation': 'DEFAULT123',
                                     })
        self.assertEqual(response.data, dumps(
            {'detail': 'different password'}))

    def test_different_password(self):
        response = self.client.post('/api/auth/password/',
                                    {'userid': self.user.pk,
                                     'password': 'default123',
                                     'new_password': 'DEFAULT123',
                                     'new_password_confirmation': 'DEFAULT123',
                                     })
        self.assertEqual(response.data, dumps(
            {'detail': 'invalid password'}))

    def test_not_found_user(self):
        response = self.client.post('/api/auth/password/',
                                    {'userid': self.user.pk + 1,
                                     'password': 'DEFAULT123',
                                     'new_password': 'DEFAULT123',
                                     'new_password_confirmation': 'DEFAULT123',
                                     })
        self.assertEqual(response.data, dumps(
            {'detail': 'user not found'}))


class ClientUserTest(TestCase):

    def setUp(self):
        self.active_client = ActiveClientMainFactory()
        self.user = User.objects.last()

    def test_username_client(self):
        self.assertEqual(self.active_client.cpf, self.user.username)

    def test_check_password(self):
        self.assertTrue(self.user.check_password('default123'))
