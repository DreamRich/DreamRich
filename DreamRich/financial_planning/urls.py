from rest_framework import routers
from financial_planning.views import (
    RegularCostViewSet,
    CostManagerViewSet,
)


app_name = 'financial_planning'

router = routers.DefaultRouter()
router.register(r'^regularcost', RegularCostViewSet)
router.register(r'^costmanager', CostManagerViewSet)

urlpatterns = router.urls
