from rest_framework import routers
from employee.views import EmployeeViewSet, FinancialAdviserViewSet

app_name = 'employee'

router = routers.DefaultRouter()
router.register(r'^employee', EmployeeViewSet)
router.register(r'^financial', FinancialAdviserViewSet)

urlpatterns = router.urls
