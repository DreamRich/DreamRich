from rest_framework import routers
from employee.views import EmployeeViewSet, FinancialAdviserViewSet

APP_NAME = 'employee'  # pylint: disable=invalid-name

ROUTER = routers.DefaultRouter()  # pylint: disable=invalid-name
ROUTER.register(r'^employee', EmployeeViewSet)
ROUTER.register(r'^financial', FinancialAdviserViewSet)

urlpatterns = ROUTER.urls
