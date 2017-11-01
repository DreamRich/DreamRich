from json import dumps
from django.test import TestCase, Client as ClientTest
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from client.factories import ActiveClientMainFactory
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory,
)


class AuthTest(TestCase):

    def setUp(self):
        self.employee = EmployeeMainFactory()
        self.financial_adviser = FinancialAdviserMainFactory()
        self.active_client = ActiveClientMainFactory()
        self.client_test = ClientTest()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self.employee)
        self.token = jwt_encode_handler(payload)

    def test_get_token(self):
        response = self.client_test.post('/api/auth/',
                                         {'username': self.employee.username,
                                          'password': 'def123'})
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data['token'] is not None)

    def test_permission_employee(self):
        response = self.client_test.post('/api/auth/',
                                         {'username': self.employee.username,
                                          'password': 'def123'})
        permissions_string = response.data['permissions']
        string_compare = ('allow_any, see_all_basic_client_data, '
                          'see_employee_data')
        self.assertEqual(permissions_string, string_compare)

    def test_permission_financial_adviser(self):
        response = self.client_test.post('/api/auth/',
                                         {'username': self.financial_adviser
                                          .username,
                                          'password': 'def123'})
        self.assertEqual(
            response.data['permissions'], 'allow_any, '
            'change_own_client_data, see_all_basic_client_data, '
            'see_employee_data, see_financial_adviser_data, '
            'see_own_client_data'
        )

    def test_permission_active_client(self):
        response = self.client_test.post('/api/auth/',
                                         {'username': self.active_client
                                          .username,
                                          'password': 'default123'})
        self.assertEqual(
            response.data['permissions'], 'allow_any, see_own_client_data')

    def test_not_get_token(self):
        response = self.client_test.post('/api/auth/',
                                         {'username': self.employee.username,
                                          'password': 'DEFAULT123'})
        self.assertEqual(response.status_code, 400)


class PasswordChange(TestCase):

    def setUp(self):
        self.user = EmployeeMainFactory()
        self.client_test = ClientTest()

    def test_user_change_password(self):
        response = self.client_test.post('/api/auth/password/',
                                         {'userid': self.user.pk,
                                          'password': 'def123',
                                          'new_password': 'DEFAULT123',
                                          'new_password_confirmation':
                                          'DEFAULT123',
                                          })

        self.assertEqual(response.data, dumps({'detail': 'password changed'}))

    def test_user_match_change_password(self):
        self.client_test.post('/api/auth/password/',
                              {'userid': self.user.pk,
                               'password': 'def123',
                               'new_password': 'DEFAULT123',
                               'new_password_confirmation': 'DEFAULT123',
                               })
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password('DEFAULT123'))

    def test_different_passwords(self):
        response = self.client_test.post('/api/auth/password/',
                                         {'userid': self.user.pk,
                                          'password': 'def123',
                                          'new_password': 'default123',
                                          'new_password_confirmation':
                                          'DEFAULT123',
                                          })
        self.assertEqual(response.data, dumps(
            {'detail': 'different password'}))

    def test_different_password(self):
        response = self.client_test.post('/api/auth/password/',
                                         {'userid': self.user.pk,
                                          'password': 'default123',
                                          'new_password': 'DEFAULT123',
                                          'new_password_confirmation':
                                          'DEFAULT123',
                                          })
        self.assertEqual(response.data, dumps(
            {'detail': 'invalid password'}))

    def test_not_found_user(self):
        response = self.client_test.post('/api/auth/password/',
                                         {'userid': self.user.pk + 1,
                                          'password': 'DEFAULT123',
                                          'new_password': 'DEFAULT123',
                                          'new_password_confirmation':
                                          'DEFAULT123',
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
