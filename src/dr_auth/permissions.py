from rest_framework.permissions import BasePermission
from dreamrich.utils import Relationship


class ClientsPermissions(BasePermission):

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
            authorized = True

        return authorized


class EmployeesPermissions(BasePermission):

    def has_permission(self, request, view):
        return True


class FinancialAdvisersPermissions(BasePermission):

    def has_permission(self, request, view):
        return True


class GeneralPermissions(BasePermission):

    def has_permission(self, request, view):
        return True
