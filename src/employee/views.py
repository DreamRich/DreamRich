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
    """
    retrieve:
        Return a employee instance.

    list:
        Return all employees, ordered by most recently joined.

    create:
        Create a new employee.

    delete:
        Remove an existing employee.

    partial_update:
        Update one or more fields on an existing employee.

    update:
        Update a employee.
    """

    required_permission = 'see_employee_data'
    permission_classes = (EmployeesPermission,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class FinancialAdviserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a financial adviser.

    list:
        Return all financial advisers, ordered by most recently joined.

    create:
        Create a new financial adviser.

    delete:
        Remove an existing financial adviser.

    partial_update:
        Update one or more fields on an existing financial adviser.

    update:
        Update a financial adviser.
    """

    required_permission = 'see_employee_data'

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (FinancialAdvisersPermission,)
