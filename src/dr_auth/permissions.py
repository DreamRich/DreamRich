from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoModelPermissions


class ClientsModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['client.see_client'],
        'POST': ['client.add_client'],
        'PUT': ['client.change_client'],
        'PATCH': ['client.change_client'],
        'DELETE': ['client.delete_client'],
    }


class EmployeesModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['employee.see_employee'],
        'POST': ['employee.add_employee'],
        'PUT': ['employee.change_employee'],
        'PATCH': ['employee.change_employee'],
        'DELETE': ['employee.delete_employee'],
    }


class FinancialAdvisersModelPermissions(DjangoModelPermissions):
    # fa = financial adviser
    perms_map = {
        'GET': ['fa.see_fa'],
        'POST': ['fa.add_fa'],
        'PUT': ['fa.change_fa'],
        'PATCH': ['fa.change_fa'],
        'DELETE': ['fa.delete_fa'],
    }


class GeneralModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['general.see_general'],
        'POST': ['general.add_general'],
        'PUT': ['general.change_general'],
        'PATCH': ['general.change_general'],
        'DELETE': ['general.delete_general'],
    }


class ClientsCustomPermissions(BasePermission):

    def has_permission(self, request, view):
        user_pk = str(request.user.pk)

        if (request.user.has_perm('client.see_own_client') and
                view.action == 'retrieve' and
                view.kwargs['pk'] == user_pk):
            authorized = True
        elif (request.user.has_perm('client.change_own_client') and
                (view.action == 'update' or
                 view.action == 'partial_update') and
                view.kwargs['pk'] == user_pk):
            authorized = True
        else:
            authorized = False

        return authorized


class EmployeesCustomPermissions(BasePermission):

    def has_permission(self, request, view):
        return False


class FinancialAdvisersCustomPermissions(BasePermission):

    def has_permission(self, request, view):
        return False


class GeneralCustomPermissions(BasePermission):

    def has_permission(self, request, view):
        return False
