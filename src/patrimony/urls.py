from rest_framework import routers
from patrimony.views import (
    PatrimonyViewSet,
    ActiveViewSet,
    ArrearageViewSet,
    RealStateViewSet,
    CompanyParticipationViewSet,
    EquipmentViewSet,
    IncomeViewSet,
    ActiveTypeViewSet,
    ActiveManagerViewSet,
    ActiveChartDetailView,
)


APP_NAME = 'patrimony'

ROUTER = routers.DefaultRouter()
ROUTER.register(r'active', ActiveViewSet)
ROUTER.register(r'active-type', ActiveTypeViewSet)
ROUTER.register(r'active-manager', ActiveManagerViewSet)
ROUTER.register(r'active-chart', ActiveChartDetailView)
ROUTER.register(r'arrearage', ArrearageViewSet)
ROUTER.register(r'real-state', RealStateViewSet)
ROUTER.register(r'company-participation', CompanyParticipationViewSet)
ROUTER.register(r'equipment', EquipmentViewSet)
ROUTER.register(r'income', IncomeViewSet)
ROUTER.register(r'', PatrimonyViewSet)

urlpatterns = ROUTER.urls
