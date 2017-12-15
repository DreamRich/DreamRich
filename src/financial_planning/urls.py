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
ROUTER.register(r'^regular_cost', RegularCostViewSet)
ROUTER.register(r'^cost_manager', CostManagerViewSet)
ROUTER.register(r'financial_planning', FinancialPlanningViewSet)
ROUTER.register(r'unit_change', FlowUnitChangeViewSet)
ROUTER.register(r'financial_independence', FinancialIndependenceViewSet)

urlpatterns = [url(r'cost_type/$', CostTypeViewList.as_view())] + ROUTER.urls
