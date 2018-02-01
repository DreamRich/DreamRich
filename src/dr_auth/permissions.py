from rest_framework.permissions import BasePermission
from dreamrich.utils import Relationship


class BaseCustomPermissions(BasePermission):

    class Meta:
        abstract = True

    authorized = False
    view = None
    request = None
    user = None

    # Same used when defining models permissions
    app_name = ''
    checked_name = ''

    _not_implemented_error_message = ('This method must be implemented at all'
                                      ' children classes')

    def has_permission(self, request, view):
        self.view = view
        self.request = request
        self.user = self.request.user

        self._check_children_params()

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

    def to_own(self, action, app, user):
        user_pk = str(self.user.pk)
        consulted_pk = self.view.kwargs['pk']

        permission_name = '{}.{}_own_{}'.format(app, action, user)
        
        if self.user.has_perm(permission_name) and user_pk == consulted_pk:
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


class EmployeesPermissions(BaseCustomPermissions):

    app_name = 'employee'
    checked_name = 'employees'


class FinancialAdvisersPermissions(BaseCustomPermissions):

    app_name = 'employee'
    checked_name = 'fa'


class GeneralPermissions(BaseCustomPermissions):

    app_name = 'dreamrich'
    checked_name = 'general'
