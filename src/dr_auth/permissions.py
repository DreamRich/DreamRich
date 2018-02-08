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
        if request.user.is_authenticated():
            self._check_children_params()

            self.view = view
            self.request = request
            self.user = self.get_user_original_object()

            return self.has_permission_to(self.view.action)
        return False

    def has_permission_to(self, permission_action):
        permission_action = ('update' if permission_action == 'partial_update'
                             else permission_action)

        allowed_permissions = [
            '{}.{}_{}_{}'.format(
                self.app_name, permission_action, ownership, self.checked_name
            ) for ownership in ('all', 'any', 'related')
        ]

        related_permission = allowed_permissions.pop()
        has_related_permission = self.has_any_permission(related_permission)

        return (self.has_any_permission(*allowed_permissions) or
                has_related_permission and self.has_passed_related_checks())

    def has_any_permission(self, *permissions_codenames):
        for permission in permissions_codenames:
            if self.request.user.has_perm(permission):
                return True
        return False

    def has_passed_related_checks(self):
        self._fill_consulted_attr()

        # Should be one checker for each user
        # Override called methods to get personalized checks
        related_checkers = {
            'ActiveClient': self.related_activeclient_checker,
            'Employee': self.related_employee_checker,
            'FinancialAdviser': self.related_financialadviser_checker,
        }
        try:
            checker_function = related_checkers[self.user.__class__.__name__]
            passed_checker = checker_function()
        except KeyError:
            raise AttributeError('User not listed at checkers'
                                 'has made a request.')

        return passed_checker

    # We want, for example, an ActiveClient and not an User instance
    def get_user_original_object(self):
        user = self.request.user

        for model in self._users_models:
            try:
                user_object = model.objects.get(username=user.username)
                break
            except ObjectDoesNotExist:
                pass
        else:
            raise ObjectDoesNotExist("Couldn't find user model"
                                     " for the user provided.")
        return user_object

    def _check_children_params(self):
        required_params = {self.app_name: 'app_name',
                           self.checked_name: 'checked_name'}

        if not all(required_params.keys()):
            raise AttributeError('Attribute {} was not filled at child class')

    # To be used for children classes
    def _fill_consulted_attr(self):
        self.consulted = None

        # Http methods which are not directed to specific instances would raise
        # exception
        if self.view.action not in ('list', 'post'):
            self.consulted = self.view.get_object()

    def related_activeclient_checker(self):  # pylint: disable=no-self-use
        return False

    def related_employee_checker(self):  # pylint: disable=no-self-use
        return False

    def related_financialadviser_checker(self):  # pylint: disable=no-self-use
        return False


class ClientsPermissions(BaseCustomPermissions):

    app_name = 'client'
    checked_name = 'clients'

    def related_activeclient_checker(self):
        return self.user.pk == self.consulted.pk

    def related_financialadviser_checker(self):
        relationship = Relationship(self.consulted, self.user,
                                    related_name='clients')

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
