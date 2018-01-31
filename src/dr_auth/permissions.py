from rest_framework.permissions import BasePermission
from dreamrich.utils import Relationship


class BaseCustomPermissions(BasePermission):

    class Meta:
        abstract = True

    authorized = False
    view = None
    request = None
    user = None

    _not_implemented_error_message = ('This method must be implemented at all'
                                      ' children classes')

    def has_permission(self, request, view):
        self.view = view
        self.request = request
        self.user = self.request.user

        authorized = False
        if view.action == 'list':
            authorized = self.list()
        elif view.action == 'retrieve':
            authorized = self.retrieve()
        elif view.action == 'create':
            authorized = self.create()
        elif view.action in ('update', 'partial_update'):
            authorized = self.update()
        elif view.action == 'destroy':
            authorized = self.destroy()

        return authorized

    def list(self):
        raise NotImplementedError(self._not_implemented_error_message)

    def retrieve(self):
        raise NotImplementedError(self._not_implemented_error_message)

    def create(self):
        raise NotImplementedError(self._not_implemented_error_message)

    def update(self):
        raise NotImplementedError(self._not_implemented_error_message)

    def destroy(self):
        raise NotImplementedError(self._not_implemented_error_message)


class ClientsPermissions(BaseCustomPermissions):

    def list(self):
        return False

    def retrieve(self):
        return False

    def create(self):
        return False

    def update(self):
        return False

    def destroy(self):
        return False


class EmployeesPermissions(BaseCustomPermissions):

    def list(self):
        return False

    def retrieve(self):
        return False

    def create(self):
        return False

    def update(self):
        return False

    def destroy(self):
        return False


class FinancialAdvisersPermissions(BaseCustomPermissions):

    def list(self):
        return False

    def retrieve(self):
        return False

    def create(self):
        return False

    def update(self):
        return False

    def destroy(self):
        return False


class GeneralPermissions(BaseCustomPermissions):

    def list(self):
        return False

    def retrieve(self):
        return False

    def create(self):
        return False

    def update(self):
        return False

    def destroy(self):
        return False
