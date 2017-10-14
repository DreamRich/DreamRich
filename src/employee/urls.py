from rest_framework import routers
from employee.views import EmployeeViewSet, FinancialAdviserViewSet

app_name = 'employee' # pylint: disable=invalid-name

router = routers.DefaultRouter() # pylint: disable=invalid-name
router.register(r'^employee', EmployeeViewSet)
router.register(r'^financial', FinancialAdviserViewSet)

urlpatterns = router.urls
