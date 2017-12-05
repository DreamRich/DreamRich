import json
from django.test import TestCase
from dreamrich.utils import get_token
from rest_framework.test import APIClient
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)


# Default user is employee, but the class can be imported and other user used
# User is the one who will make the requests
class EmployeePermissionsTest(TestCase):

    def setUp(self, user=None):  # pylint: disable=arguments-differ
        self.django_client = APIClient()
        self.employee = EmployeeMainFactory()
        self.other_employee = EmployeeMainFactory()

        # Authenticate user
        self.user = self.employee if not user else user

        user_token = get_token(self.user)
        self.token = 'JWT {}'.format(user_token)
        self.django_client.credentials(HTTP_AUTHORIZATION=self.token)

    @staticmethod
    def get_route(element=0):
        route = '/api/employee/employee/'
        route += '{}/'.format(element) if element else ''

        return route

    def test_employee_get_itself(self):
        route = self.get_route(element=self.user.id)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_employee_put_itself(self):
        route = self.get_route(element=self.user.id)

        response = self.django_client.put(
            route,
            json.dumps({
                'first_name': 'Maria',
                'last_name': 'Old',
                'cpf': '72986145094',
                'email': ''
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_employee_patch_itself(self):
        route = self.get_route(element=self.user.id)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Old',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_employee_delete_itself(self):
        route = self.get_route(element=self.user.id)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 403)

    def test_user_get_employee(self, status_code=403):
        route = self.get_route(element=self.other_employee.id)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, status_code)

    def test_user_put_employee(self, status_code=403):
        other_employee_id = self.other_employee.id
        route = self.get_route(other_employee_id)

        response = self.django_client.put(
            route,
            json.dumps({
                'id': other_employee_id,
                'first_name': 'Maria',
                'last_name': 'Old',
                'cpf': '72986145094',
                'email': ''
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)

    def test_user_patch_employee(self, status_code=403):
        route = self.get_route(element=self.other_employee.id)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Old',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)

    def test_user_delete_employee(self, status_code=403):
        route = self.get_route(element=self.other_employee.id)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, status_code)

    def test_employee_get_list(self, status_code=403):
        route = self.get_route()
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, status_code)

    def test_employee_post(self, status_code=403):
        route = self.get_route()

        response = self.django_client.post(
            route,
            json.dumps({
                'first_name': 'Maria',
                'last_name': 'Old',
                'cpf': '72986145094',
                'email': ''
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)


class FinancialAdviserPermissionsTest(TestCase):

    def setUp(self, user=None):  # pylint: disable=arguments-differ
        self.django_client = APIClient()
        self.financial_adviser = FinancialAdviserMainFactory()
        self.other_financial_adviser = FinancialAdviserMainFactory()

        # Authenticate user
        self.user = self.financial_adviser if not user else user

        user_token = get_token(self.user)
        self.token = 'JWT {}'.format(user_token)
        self.django_client.credentials(HTTP_AUTHORIZATION=self.token)

    @staticmethod
    def get_route(element=0):
        route = '/api/employee/financial/'

        if element:
            route += '{}/'.format(element)
        else:
            route = route

        return route

    def test_financial_adviser_get_own_data(self):
        route = self.get_route(self.financial_adviser.pk)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_financial_adviser_put_own_data(self):
        route = self.get_route(self.financial_adviser.pk)

        response = self.django_client.put(
            route,
            json.dumps({
                'first_name': 'Jeremy',
                'last_name': 'Dixon',
                'cpf': '68205793492',
                'email': ''
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_financial_adviser_patch_own_data(self):
        route = self.get_route(self.financial_adviser.pk)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Lee',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_financial_adviser_delete_own_data(self):
        route = self.get_route(self.financial_adviser.pk)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 204)

    def test_user_get_financial_adviser(self, status_code=200):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self.get_route(other_financial_adviser_pk)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, status_code)

    def test_user_put_financial_adviser(self, status_code=200):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self.get_route(other_financial_adviser_pk)

        response = self.django_client.put(
            route,
            json.dumps({
                'pk': other_financial_adviser_pk,
                'first_name': 'Maria',
                'last_name': 'Old',
                'cpf': '72986145094',
                'email': ''
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)

    def test_user_patch_financial_adviser(self, status_code=200):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self.get_route(other_financial_adviser_pk)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Old',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)

    def test_user_delete_financial_adviser(self, status_code=200):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self.get_route(other_financial_adviser_pk)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, status_code)

    def test_get_list_financial_advisers(self, status_code=200):
        route = self.get_route()

        response = self.django_client.get(route)

        self.assertEqual(response.status_code, status_code)

    def test_post_financial_adviser(self, status_code=200):
        route = self.get_route()

        response = self.django_client.post(
            route,
            json.dumps({
                'first_name': 'Jeremy',
                'last_name': 'Dixon',
                'cpf': '68205793492',
                'email': ''
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status_code)
