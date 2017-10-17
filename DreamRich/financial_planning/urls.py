from rest_framework import routers
from django.conf.urls import url
from financial_planning.views import (
    RegularCostViewSet,
    CostTypeViewList,
    CostManagerViewSet,
)


app_name = 'financial_planning' # pylint: disable=invalid-name

router = routers.DefaultRouter() # pylint: disable=invalid-name
router.register(r'^regular_cost', RegularCostViewSet)
router.register(r'^cost_manager', CostManagerViewSet)


urlpatterns = [url(r'cost_type/$', CostTypeViewList.as_view())] + router.urls
