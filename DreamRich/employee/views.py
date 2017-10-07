from rest_framework import viewsets
from dr_auth.roles import *
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer,
)
from employee.models import (
    Employee,
    FinancialAdviser,
)
from dr_auth.permissions import SomePermission, EmployeesPermission  

class EmployeeViewSet(viewsets.ModelViewSet):
    required_permission = 'see_employee_data'
    permission_classes = (EmployeesPermission,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    @list_route(methods=['get']) 
    def employee_permissions(self, request):
        queryset = Employee.objects.all()
        employee_available_permissions = CommonEmployee().available_permissions 
        return Response(employee_available_permissions)
    @detail_route
    def a(self, request, *args, **kwargs):
        print(request.user)

class FinancialAdviserViewSet(viewsets.ModelViewSet):
    required_permission = 'see_financialadvisers_data'

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (EmployeesPermission,)

    @detail_route(methods=['get'])
    def a(self, request, pk=None, *args, **kwargs):
        print(request.user)
        return None
