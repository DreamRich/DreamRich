from rest_framework import permissions
import rolepermissions
from rolepermissions import checkers

class EmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        current_user = view.queryset.filter(id=request.user.id).get()
        print(request.user.id)
        if not checkers.has_permission(request.user, 'see_financialadvisers_data'):
            view.queryset = view.queryset.values().filter(id=request.user.id)
        return True

class ClientsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if checkers.has_permission(request.user, 'change_own_client_data'):
            return True
        return False 

