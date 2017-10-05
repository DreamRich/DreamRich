from rest_framework import permissions
import rolepermissions
from rolepermissions import checkers
class EmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        current_user = view.queryset.filter(id=request.user.id).get()
        if not hasattr(current_user,"financialadviser"):
            view.queryset = view.queryset.values().filter(id=request.user.id)
        return True


class SomePermission(permissions.BasePermission):
    message = 'My custom permission'

    def has_permission(self, request, view):
        user = request.user
        print(view)
        if checkers.has_permission(user,'create_employee'):
            print("uhuuu")
        permissions = rolepermissions.permissions.available_perm_status(user)
        print("alooo",view.required_permission, permissions)
        print(user)
        if view.required_permission in permissions:
            a = permissions[view.required_permission]
            print(a)
            return a
        return False

'''class CommonEmployeePermission(permissions.BasePermission):
    
    def has_permission(self, request, view):'''
        
        
