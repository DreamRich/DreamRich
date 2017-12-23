from rest_framework.permissions import BasePermission


class FinancialAdvisersPermission(BasePermission):
    def has_permission(self, request, view):
        return False


class EmployeesPermission(BasePermission):
    def has_permission(self, request, view):
        return False


class ClientsPermission(BasePermission):
    def has_permission(self, request, view):
        return False


class FinancialPlanningPermission:

    @staticmethod
    def has_permission_to_see_chart(request_user):
        return True
