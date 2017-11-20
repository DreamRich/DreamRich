from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_permission


class FinancialAdvisersPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission(request.user, 'see_financial_adviser_data')


class EmployeesPermission(BasePermission):
    def has_permission(self, request, view):
        if (has_permission(request.user, 'see_employee_data') and not
                has_permission(request.user, 'see_financial_adviser_data')):
            view.queryset = view.queryset.filter(id=request.user.id)
            return True
        return False


class ClientsPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission(request.user, 'change_own_client_data')
