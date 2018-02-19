from rest_framework import routers
from employee.views import EmployeeViewSet, FinancialAdviserViewSet

APP_NAME = 'employee'

ROUTER = routers.DefaultRouter()
ROUTER.register(r'employee', EmployeeViewSet)
ROUTER.register(r'financial-adviser', FinancialAdviserViewSet)

urlpatterns = ROUTER.urls
