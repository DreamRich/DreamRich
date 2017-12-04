import json
from django.test import TestCase
from dreamrich.utils import get_token
from rest_framework.test import APIClient
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)


class EmployeePermissionsTest(TestCase):

    def setUp(self):
        self.django_client = APIClient()
        self.employee = EmployeeMainFactory()
        self.other_employee = EmployeeMainFactory()

        # Authenticate user
        self.token = 'JWT {}'.format(get_token(self.employee))
        self.django_client.credentials(HTTP_AUTHORIZATION=self.token)

    @staticmethod
    def _get_route(element=0):
        route = '/api/employee/employee/'

        if element:
            route += '{}/'.format(element)
        else:
            route = route

        return route

    def test_employee_own_data_get(self):
        route = self._get_route(element=self.employee.id)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_employee_own_data_put(self):
        route = self._get_route(element=self.employee.id)

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

    def test_employee_own_data_patch(self):
        route = self._get_route(element=self.employee.id)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Old',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_employee_own_data_delete(self):
        route = self._get_route(element=self.employee.id)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 403)

    def test_employee_get_other_employee_data(self):
        route = self._get_route(element=self.other_employee.id)

        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 403)

    def test_employee_put_other_employee_data(self):
        other_employee_id = self.other_employee.id
        route = self._get_route(other_employee_id)

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

        self.assertEqual(response.status_code, 403)

    def test_employee_patch_other_employee_data(self):
        route = self._get_route(element=self.other_employee.id)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Old',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)

    def test_employee_delete_other_employee_data(self):
        route = self._get_route(element=self.other_employee.id)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 403)

    def test_employee_get_list(self):
        route = self._get_route()

        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 403)

    def test_employee_post(self):
        route = self._get_route()

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

        self.assertEqual(response.status_code, 403)


class FinancialAdviserPermissionsTest(TestCase):

    def setUp(self):
        self.django_client = APIClient()
        self.financial_adviser = FinancialAdviserMainFactory()
        self.other_financial_adviser = FinancialAdviserMainFactory()

        # Authenticate user
        self.token = 'JWT {}'.format(get_token(self.financial_adviser))
        self.django_client.credentials(HTTP_AUTHORIZATION=self.token)

    @staticmethod
    def _get_route(element=0):
        route = '/api/employee/financial/'

        if element:
            route += '{}/'.format(element)
        else:
            route = route

        return route

    def test_financial_adviser_own_data_get(self):
        route = self._get_route(self.financial_adviser.pk)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_financial_adviser_own_data_put(self):
        route = self._get_route(self.financial_adviser.pk)

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

    def test_financial_adviser_own_data_patch(self):
        route = self._get_route(self.financial_adviser.pk)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Lee',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_financial_adviser_own_data_delete(self):
        route = self._get_route(self.financial_adviser.pk)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 204)

    def test_get_other_financial_adviser_data(self):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self._get_route(other_financial_adviser_pk)
        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_put_other_financial_adviser_data(self):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self._get_route(other_financial_adviser_pk)

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

        self.assertEqual(response.status_code, 200)

    def test_patch_other_financial_adviser_data(self):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self._get_route(other_financial_adviser_pk)

        response = self.django_client.patch(
            route,
            json.dumps({
                'last_name': 'Old',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_other_financial_adviser_data(self):
        other_financial_adviser_pk = self.other_financial_adviser.pk

        route = self._get_route(other_financial_adviser_pk)
        response = self.django_client.delete(route)

        self.assertEqual(response.status_code, 204)

    def test_financial_adviser_get_list(self):
        route = self._get_route()

        response = self.django_client.get(route)

        self.assertEqual(response.status_code, 200)

    def test_financial_adviser_post(self):
        route = self._get_route()

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

        self.assertEqual(response.status_code, 201)
