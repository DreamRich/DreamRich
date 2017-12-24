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


class EmployeeModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['employee.see_employee'],
        'POST': ['employee.add_employee'],
        'PUT': ['employee.change_employee'],
        'PATCH': ['employee.change_employee'],
        'DELETE': ['employee.delete_employee'],
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
