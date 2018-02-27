import json
from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from rest_framework.routers import SimpleRouter
from rest_framework.test import APIClient
from employee.views import (
    EmployeeViewSet,
    FinancialAdviserViewSet
)
from employee.factories import EmployeeFactory, FinancialAdviserFactory
from client.factories import ActiveClientFactory
from client.views import ActiveClientViewSet
from financial_planning.views import FinancialPlanningViewSet
from financial_planning.factories import FinancialPlanningFactory
from dreamrich.utils import Relationship
from dreamrich.complete_factories import (
    ActiveClientCompleteFactory,
    FinancialAdviserCompleteFactory
)
from .utils import authenticate_user


class PermissionsTests(TestCase):

    # Children will fill these attributes
    factory_consulted = None
    factory_user = None
    serializer_consulted = None
    authenticated_user = None
    base_route = ''

    related_name = ''
    related_names = ('',)

    httpmethod_by_action = dict(
        retrieve='get', create='post', update='put', partial_update='patch',
        destroy='delete', list='get'
    )

    to_itself = False

    def setUp(self):
        def get_fill_attr_exception(attr):
            return AttributeError("Fill '{}' at child class.".format(attr))

        try:
            # pylint: disable=not-callable
            self.user = self.factory_user()
        except TypeError:
            raise get_fill_attr_exception('factory_user')

        if self.to_itself:
            self.consulted = self.user
        else:
            try:
                # pylint: disable=not-callable
                self.consulted = self.factory_consulted()
            except TypeError:
                raise get_fill_attr_exception('factory_consulted')

        self.serializer_consulted = self.view_consulted.serializer_class
        self.handle_related()

    def user_test_request(self, action, status_code):
        self.authenticated_user = authenticate_user(self.user)
        response_status_code = self.make_request(action)

        self.assertEqual(response_status_code, status_code)

    def user_test_not_authenticated_request(self, action):
        self.authenticated_user = APIClient()
        response_status_code = self.make_request(action)

        self.assertEqual(response_status_code, HTTPStatus.UNAUTHORIZED)

    def make_request(self, action, route=None):
        route = self._get_route(action) if not route else route

        api_client_method = getattr(self.authenticated_user,
                                    self.httpmethod_by_action[action])

        # Prepare data and make request
        if action in ('create', 'update', 'partial_update'):
            response = self._make_required_data_request(
                action, api_client_method, route
            )
        else:
            response = api_client_method(route)

        return response.status_code

    def handle_related(self):
        if self.related_name:
            relationship = Relationship(
                self.user,
                related_name=self.related_name
            )
            self.consulted = relationship.get_related()
        elif self.related_names[0]:
            relationship = Relationship(
                self.user,
                related_name=self.related_names[0]
            )
            related_metas = tuple(
                Relationship.RelatedMeta(related_name, None)
                for related_name in self.related_names
            )
            self.consulted = relationship.get_nested_related(*related_metas)

    def _make_required_data_request(self, action, api_client_method, route):
        data = self._get_data()

        if action == 'partial_update':
            field = (data.popitem(),)
            data = dict(field)
        elif action == 'create':
            self.consulted.delete()

        data = json.dumps(data)
        response = api_client_method(
            route, data, content_type='application/json'
        )

        return response

    def _get_route(self, action):
        router = SimpleRouter()

        try:
            base_name = router.get_default_base_name(self.view_consulted)
        except AssertionError:
            raise AttributeError(
                "If your routes don't follow the standards given for routers,"
                " override this method."
            )

        pk_kwarg = {'pk': self.consulted.pk}

        return (reverse(base_name + '-list') if action in ('create', 'list')
                else reverse(base_name + '-detail', kwargs=pk_kwarg))

    def _get_data(self):
        serialized_class = self.serializer_consulted(self.consulted)
        fields = serialized_class.get_fields()
        read_only_fields = self._get_read_only_fields(fields)

        data = serialized_class.data
        data = self._remove_read_only_fields(data, read_only_fields)

        return data

    @staticmethod
    def _remove_read_only_fields(data, read_only_fields):
        for field in read_only_fields:
            data.pop(field, None)

        return data

    @staticmethod
    def _get_read_only_fields(fields):
        all_fields_names = list(fields.keys())

        # Get all fields with read_only == True
        read_only_fields = [name for name in all_fields_names
                            if fields[name].read_only]

        # Remove id's fields
        read_only_fields = [field for field in read_only_fields
                            if field[-3:] != '_id']

        return read_only_fields


class ClientToModel:

    factory_user = ActiveClientCompleteFactory


class EmployeeToModel:

    factory_user = EmployeeFactory


class FinancialAdviserToModel:

    factory_user = FinancialAdviserCompleteFactory


class UserToClient:

    factory_consulted = ActiveClientFactory
    view_consulted = ActiveClientViewSet


class UserToEmployee:

    factory_consulted = EmployeeFactory
    view_consulted = EmployeeViewSet


class UserToFinancialAdviser:

    factory_consulted = FinancialAdviserFactory
    view_consulted = FinancialAdviserViewSet


# Refer to all others classes which have the same permissions
# Financial Planning was chosen for convenience
class UserToGeneral:

    factory_consulted = FinancialPlanningFactory
    view_consulted = FinancialPlanningViewSet
