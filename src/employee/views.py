from rest_framework import viewsets
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer,
)
from employee.models import (
    Employee,
    FinancialAdviser,
)
from dr_auth.permissions import (
    EmployeesPermission,
    FinancialAdvisersPermission
)


class EmployeeViewSet(viewsets.ModelViewSet):
    required_permission = 'see_employee_data'
    permission_classes = (EmployeesPermission,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class FinancialAdviserViewSet(viewsets.ModelViewSet):
    required_permission = 'see_employee_data'

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (FinancialAdvisersPermission,)
