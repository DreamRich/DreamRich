from rest_framework import viewsets
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer,
)
from employee.models import (
    Employee,
    FinancialAdviser,
)
from dr_auth.models_permissions import (
    EmployeesModelPermissions,
    FinancialAdvisersModelPermissions,
)
from dr_auth.custom_permissions import (
    EmployeesCustomPermissions,
    FinancialAdvisersCustomPermissions
)


class EmployeeViewSet(viewsets.ModelViewSet):

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = (EmployeesModelPermissions,
                          EmployeesCustomPermissions)


class FinancialAdviserViewSet(viewsets.ModelViewSet):

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (FinancialAdvisersModelPermissions,
                          FinancialAdvisersCustomPermissions)
