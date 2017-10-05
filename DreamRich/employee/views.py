from rest_framework import viewsets
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
    required_permission = 'see_client_basic_data'
    permission_classes = (EmployeesPermission,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    @detail_route
    def a(self, request, *args, **kwargs):
        print(request.user)


class FinancialAdviserViewSet(viewsets.ModelViewSet):
    required_permission = {'change_client_data'}

    serializer_class = FinancialAdviserSerializer
    queryset = FinancialAdviser.objects.all()
    permission_classes = (EmployeesPermission,)

    @detail_route(methods=['get'])
    def a(self, request, pk=None, *args, **kwargs):
        print(request.user)
        return None
