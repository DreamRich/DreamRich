from rest_framework import routers
from django.conf.urls import url
from financial_planning.views import (
    RegularCostViewSet,
    CostTypeViewList,
    CostManagerViewSet,
    FinancialPlanningViewSet,
    FlowUnitChangeViewSet,
    FinancialIndependenceViewSet,
)


APP_NAME = 'financial_planning'

ROUTER = routers.DefaultRouter()
ROUTER.register(r'regular-cost', RegularCostViewSet)
ROUTER.register(r'cost-manager', CostManagerViewSet)
ROUTER.register(r'financial-planning', FinancialPlanningViewSet)
ROUTER.register(r'flow-unit-change', FlowUnitChangeViewSet)
ROUTER.register(r'financial-independence', FinancialIndependenceViewSet)

urlpatterns = [url(r'cost-type/$', CostTypeViewList.as_view())] + ROUTER.urls
