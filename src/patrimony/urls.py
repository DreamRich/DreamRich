from rest_framework import routers
from patrimony.views import (
    PatrimonyViewSet,
    ActiveViewSet,
    ArrearageViewSet,
    RealEstateViewSet,
    CompanyParticipationViewSet,
    EquipmentViewSet,
    LifeInsuranceViewSet,
    IncomeViewSet,
    ActiveTypeViewSet,
    ActiveManagerViewSet,
    ActiveChartDetailView,
)


APP_NAME = 'patrimony'

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^active', ActiveViewSet)
ROUTER.register(r'^active_type', ActiveTypeViewSet)
ROUTER.register(r'^active_manager', ActiveManagerViewSet)
ROUTER.register(r'^active_chart', ActiveChartDetailView)
ROUTER.register(r'^arrearage', ArrearageViewSet)
ROUTER.register(r'^realestate', RealEstateViewSet)
ROUTER.register(r'^companyparticipation', CompanyParticipationViewSet)
ROUTER.register(r'^equipment', EquipmentViewSet)
ROUTER.register(r'^lifeinsurance', LifeInsuranceViewSet)
ROUTER.register(r'^income', IncomeViewSet)
ROUTER.register(r'', PatrimonyViewSet)

urlpatterns = ROUTER.urls
