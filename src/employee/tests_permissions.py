from dreamrich.tests_permissions import PermissionsTests
from employee.serializers import EmployeeSerializer
from employee.factories import (
    EmployeeMainFactory,
    FinancialAdviserMainFactory
)


class UserToEmployeePermissionsTests(PermissionsTests):

    factory = EmployeeMainFactory
    serializer = EmployeeSerializer
    base_route = '/api/employee/employee/'


class EmployeeToItselfPermissionsTests(UserToEmployeePermissionsTests):

    def test_employee_get_itself(self):
        self.user_get_request(200)

    def test_employee_delete_itself(self):
        self.user_delete_request(403)

    def test_employee_put_itself(self):
        self.user_put_request(403)

    def test_employee_patch_itself(self):
        self.user_patch_request(403)


class EmployeeToEmployeePermissionsTests(UserToEmployeePermissionsTests):

    def setUp(self):
        self._initialize()
        self.consulted_instance = EmployeeMainFactory()

    def test_employee_get_employee(self):
        self.user_get_request(403)

    def test_employee_put_employee(self):
        self.user_put_request(403)

    def test_employee_patch_employee(self):
        self.user_patch_request(403)

    def test_employee_delete_employee(self):
        self.user_delete_request(403)

    def test_get_employees_list(self):
        self.user_get_list_request(403)

    def test_employee_post(self):
        self.user_post_request(403)


class EmployeeToClientPermissionsTests(TestCase):
    def setUp(self):
        self.employee = EmployeeMainFactory()

        self.client_test = client.tests_permissions.ToClientPermissionsTests()
        self.client_test.setUp(self.employee)

    def test_employee_get_client(self):
        self.client_test.test_user_get_client(status_code=403)

    def test_employee_put_client(self):
        self.client_test.test_user_put_client(status_code=403)

    def test_employee_patch_client(self):
        self.client_test.test_user_patch_client(status_code=403)

    def test_employee_delete_client(self):
        self.client_test.test_user_delete_client(status_code=403)

    def test_get_employees_list(self):
        self.client_test.test_clients_get_list(status_code=403)

    def test_employee_post(self):
        self.client_test.test_client_post(status_code=403)


class EmployeeToFinancialAdviserPermissionsTests(TestCase):
    def setUp(self):
        self.employee = EmployeeMainFactory()

        self.financial_adviser_test = ToFinancialAdviserPermissionsTests()
        self.financial_adviser_test.setUp(self.employee)

    def test_employee_get_client(self):
        self.financial_adviser_test \
        .test_user_get_financial_adviser(status_code=403)

    def test_employee_put_client(self):
        self.financial_adviser_test \
        .test_user_put_financial_adviser(status_code=403)

    def test_employee_patch_client(self):
        self.financial_adviser_test \
        .test_user_patch_financial_adviser(status_code=403)

    def test_employee_delete_client(self):
        self.financial_adviser_test \
        .test_user_delete_financial_adviser(status_code=403)

    def test_get_employees_list(self):
        self.financial_adviser_test \
        .test_financial_advisers_get_list(status_code=403)

    def test_employee_post(self):
        self.financial_adviser_test \
        .test_financial_adviser_post(status_code=403)


class ToFinancialAdviserPermissionsTests(TestCase):
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
    def get_route(consulted_instance=0):
        route = '/api/employee/financial/'

        if consulted_instance:
            route += '{}/'.format(consulted_instance)
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

    def test_financial_advisers_get_list(self, status_code=200):
        route = self.get_route()

        response = self.django_client.get(route)

        self.assertEqual(response.status_code, status_code)

    def test_financial_adviser_post(self, status_code=200):
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


class FinancialAdviserToClientPermissionsTests(TestCase):
    def setUp(self):
        self.financial_adviser = FinancialAdviserMainFactory()

        self.client_test = client.tests_permissions.ToClientPermissionsTests()
        self.client_test.setUp(self.financial_adviser)

    def test_financial_adviser_get_client(self):
        self.client_test.test_user_get_client(status_code=200)

    def test_financial_adviser_put_client(self):
        self.client_test.test_user_put_client(status_code=200)

    def test_financial_adviser_patch_client(self):
        self.client_test.test_user_patch_client(status_code=200)

    def test_financial_adviser_delete_client(self):
        self.client_test.test_user_delete_client(status_code=204)

    def test_financial_adviser_get_list(self):
        self.client_test.test_clients_get_list(status_code=200)

    def test_financial_adviser_post(self):
        self.client_test.test_client_post(status_code=201)


class FinancialAdviserToEmployeePermissionsTests(
    UserToEmployeePermissionsTests):
    def setUp(self):
        financial_adviser = FinancialAdviserMainFactory()
        authenticate_user(financial_adviser)

        self.consulted_instance = financial_adviser.id

    def test_financial_adviser_get_employee(self):
        self.user_get_employee(200)

    def test_financial_adviser_put_employee(self):
        self.user_put_employee(200)

    def test_financial_adviser_patch_employee(self):
        self.user_patch_employee(200)

    def test_financial_adviser_delete_employee(self):
        self.user_delete_employee(204)

    def test_financial_adviser_get_list(self):
        self.get_employees_list(200)

    def test_financial_adviser_post(self):
        self.employee_post(201)
