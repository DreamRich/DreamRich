from rest_framework import viewsets
from employee.serializers import (
    EmployeeSerializer,
    FinancialAdviserSerializer,
)
from employee.models import (
    Employee,
    FinancialAdviser,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

class FinancialAdviserViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
