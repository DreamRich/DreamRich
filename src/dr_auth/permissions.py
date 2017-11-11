from rest_framework import permissions
from rolepermissions import checkers


class FinancialAdvisersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if checkers.has_permission(request.user, 'see_financial_adviser_data'):
            return True
        return False


class EmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if checkers.has_permission(request.user, 'see_employee_data') \
            and not checkers.has_permission(
                request.user, 'see_financial_adviser_data'):
            view.queryset = view.queryset.values().filter(id=request.user.id)
        return True


class ClientsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if checkers.has_permission(request.user, 'change_own_client_data'):
            return True
        return False


class FinancialPlanningPermission:

    @staticmethod
    def has_permission_to_see_chart(request_user):
        if checkers.has_permission(request_user, 'see_own_client_data') and \
                checkers.has_permission(
                request_user, 'see_financial_adviser_data'):

            return True
