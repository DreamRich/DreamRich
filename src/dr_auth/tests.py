from json import dumps
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from client.factories import ActiveClientFactory
from employee.factories import EmployeeFactory
from .utils import get_token


class PasswordChange(TestCase):

    def setUp(self):
        self.user = EmployeeFactory()
        self.token = 'JWT {}'.format(get_token(self.user))

        self.django_client = APIClient()
        self.django_client.credentials(HTTP_AUTHORIZATION=self.token)

        self.password_url = reverse('password')

    def test_user_change_password(self):
        response = self.django_client.post(self.password_url,
                                           {
                                               'userid': self.user.pk,
                                               'password': 'default123',
                                               'new_password': 'DEFAULT123',
                                               'new_password_confirmation':
                                               'DEFAULT123',
                                           })

        self.assertEqual(response.data, dumps({'detail': 'password changed'}))

    def test_user_match_change_password(self):
        self.django_client.post(self.password_url,
                                {'userid': self.user.pk,
                                 'password': 'default123',
                                 'new_password': 'DEFAULT123',
                                 'new_password_confirmation': 'DEFAULT123',
                                 })

        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password('DEFAULT123'))

    def test_different_passwords(self):
        response = self.django_client.post(self.password_url,
                                           {'userid': self.user.pk,
                                            'password': 'default123',
                                            'new_password': 'default123',
                                            'new_password_confirmation':
                                            'DEFAULT123',
                                            })

        self.assertEqual(
            response.data, dumps({'detail': 'different password'})
        )

    def test_different_password(self):
        response = self.django_client.post(self.password_url,
                                           {'userid': self.user.pk,
                                            'password': 'def123',
                                            'new_password': 'DEFAULT123',
                                            'new_password_confirmation':
                                            'DEFAULT123',
                                            })
        self.assertEqual(
            response.data, dumps({'detail': 'invalid password'})
        )

    def test_not_found_user(self):
        response = self.django_client.post(self.password_url,
                                           {'userid': self.user.pk + 1,
                                            'password': 'DEFAULT123',
                                            'new_password': 'DEFAULT123',
                                            'new_password_confirmation':
                                            'DEFAULT123',
                                            })

        self.assertEqual(
            response.data, dumps({'detail': 'user not found'})
        )


class ClientUserTest(TestCase):

    def setUp(self):
        self.active_client = ActiveClientFactory()
        self.user = User.objects.last()

    def test_username_client(self):
        self.assertEqual(self.active_client.cpf, self.user.username)

    def test_check_password(self):
        self.assertTrue(self.user.check_password('default123'))
