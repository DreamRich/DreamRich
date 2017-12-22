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
        Return a employee instance.\
        Permissions: see_employee_data

    list:
        Return all employees, ordered by most recently joined.\
        Permissions: see_employee_data

    create:
        Create a new employee.\
        Permissions: see_employee_data

    delete:
        Remove an existing employee.\
        Permissions: see_employee_data

    partial_update:
        Update one or more fields on an existing employee.\
        Permissions: see_employee_data

    update:
        Update a employee.\
        Permissions: see_employee_data
    """

    required_permission = 'see_employee_data'
    permission_classes = (EmployeesPermission,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class FinancialAdviserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a financial adviser.\
        Permissions: see_employee_data

    list:
        Return all financial advisers, ordered by most recently joined.\
        Permissions: see_employee_data

    create:
        Create a new financial adviser.\
        Permissions: see_employee_data

    delete:
        Remove an existing financial adviser.\
        Permissions: see_employee_data

    partial_update:
        Update one or more fields on an existing financial adviser.\
        Permissions: see_employee_data

    update:
        Update a financial adviser.\
        Permissions: see_employee_data
    """

    required_permission = 'see_employee_data'

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (FinancialAdvisersPermission,)
