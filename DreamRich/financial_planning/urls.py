from rest_framework import routers
from financial_planning.views import (
    RegularCostViewSet,
)


app_name = 'financial_planning'

router = routers.DefaultRouter()
router.register('regularcost', RegularCostViewSet)
