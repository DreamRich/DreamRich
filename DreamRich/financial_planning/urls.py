from rest_framework import routers
from django.conf.urls import url
from financial_planning.views import (
    RegularCostViewSet,
    CostTypeViewList,
    CostManagerViewSet,
    FinancialPlanningViewSet,
)


app_name = 'financial_planning' # pylint: disable=invalid-name

router = routers.DefaultRouter() # pylint: disable=invalid-name
router.register(r'^regularcost', RegularCostViewSet)
router.register(r'^costmanager', CostManagerViewSet)
router.register(r'^financialplanning', FinancialPlanningViewSet)


urlpatterns = [url(r'costtype/$', CostTypeViewList.as_view())] + router.urls
