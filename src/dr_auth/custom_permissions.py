from rest_framework.permissions import BasePermission


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
