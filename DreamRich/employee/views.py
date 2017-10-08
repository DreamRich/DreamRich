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
from dr_auth.permissions import EmployeesPermission, FinancialAdvisersPermission


class EmployeeViewSet(viewsets.ModelViewSet):
    required_permission = 'see_employee_data'
    permission_classes = (EmployeesPermission,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    @detail_route
    def a(self, request, *args, **kwargs):
        print(request.user)


class FinancialAdviserViewSet(viewsets.ModelViewSet):
    required_permission = 'see_employee_data'

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (FinancialAdvisersPermission,)

    @detail_route(methods=['get'])
    def a(self, request, pk=None, *args, **kwargs):
        print(request.user)
        return None
