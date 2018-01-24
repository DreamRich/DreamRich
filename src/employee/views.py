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
    EmployeesPermissions,
    FinancialAdvisersPermissions
)


class EmployeeViewSet(viewsets.ModelViewSet):

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = (EmployeesPermissions,)


class FinancialAdviserViewSet(viewsets.ModelViewSet):

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (FinancialAdvisersPermissions,)
