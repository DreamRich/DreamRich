from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from client.models import ActiveClient
from employee.models import Employee, FinancialAdviser
from dreamrich.utils import Relationship


class BaseCustomPermissions(BasePermission):

    class Meta:
        abstract = True

    authorized = False
    view = None
    request = None
    user = None
    consulted = None

    # Same used when defining models permissions
    app_name = ''
    checked_name = ''

    _users_models = (ActiveClient, FinancialAdviser, Employee)
    _not_implemented_error_message = ('This method must be implemented at all'
                                      ' children classes')

    def has_permission(self, request, view):
        self._check_children_params()

        self.view = view
        self.request = request

        if str(self.request.user) == 'AnonymousUser':
            return False

        self.user = self.get_user_original_object()

        view_actions = {
            'list': self.list,
            'retrieve': self.retrieve,
            'create': self.create,
            'update': self.update,
            'partial_update': self.update,
            'destroy': self.destroy
        }

        action_method = view_actions[view.action]
        is_authorized = action_method()

        return is_authorized

    def list(self):
        return False

    def retrieve(self):
        self.consulted = self.view.get_object()

        is_authorized = any((
            self.to_own('see', self.app_name, self.checked_name),
        ))

        return is_authorized

    def create(self):
        return False

    def update(self):
        return False

    def destroy(self):
        return False

    def get_user_original_object(self):
        user = self.request.user

        for model in self._users_models:
            try:
                user_object = model.objects.get(username=user.username)
                break
            except ObjectDoesNotExist:
                pass
        else:
            raise AttributeError("Couldn't find user model"
                                 " for the user provided.")
        return user_object

    def to_own(self, action, app, user):
        # Should be one checker for each user
        related_checkers = {
            'ActiveClient': self.related_activeclient_checker,
            'Employee': self.related_employee_checker,
            'FinancialAdviser': self.related_financialadviser_checker
        }
        try:
            checker_function = related_checkers[self.user.__class__.__name__]
            passed_checker = checker_function()
        except KeyError:
            raise AttributeError('User not listed at checkers made a request.')

        possible_permissions = [
            '{}.{}_{}_{}'.format(app, action, which_clients, user)
            for which_clients in ('all', 'own')
        ]

        if self.has_any_permission(*possible_permissions) and passed_checker:
            return True
        return False

    def related_activeclient_checker(self):  # pylint: disable=no-self-use
        return False

    def related_employee_checker(self):  # pylint: disable=no-self-use
        return False

    def related_financialadviser_checker(self):  # pylint: disable=no-self-use
        return False

    def has_any_permission(self, *permissions_codenames):
        for permission in permissions_codenames:
            if self.request.user.has_perm(permission):
                return True
        return False

    def _check_children_params(self):
        required_params = {
            self.app_name: 'app_name',
            self.checked_name: 'checked_name'
        }

        if not all(required_params.keys()):
            raise AttributeError('Attribute {} was not filled at child class')


class ClientsPermissions(BaseCustomPermissions):

    app_name = 'client'
    checked_name = 'clients'

    def related_activeclient_checker(self):
        return self.user.pk == self.consulted.pk

    def related_financialadviser_checker(self):
        relationship = Relationship(self.consulted, self.user, 'clients')

        return relationship.has_relationship()


class EmployeesPermissions(BaseCustomPermissions):

    app_name = 'employee'
    checked_name = 'employees'


class FinancialAdvisersPermissions(BaseCustomPermissions):

    app_name = 'employee'
    checked_name = 'fa'


class GeneralPermissions(BaseCustomPermissions):

    app_name = 'dreamrich'
    checked_name = 'general'
