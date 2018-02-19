from rest_framework.routers import DefaultRouter
from .views import (
    EmergencyReserveViewSet,
    ProtectionManagerViewSet,
    ReserveInLackViewSet,
    ActualPatrimonySuccessionViewSet,
    IndependencePatrimonySuccessionViewSet,
    PrivatePensionViewSet,
    LifeInsuranceViewSet,
)

APP_NAME = 'protection'

ROUTER = DefaultRouter()
ROUTER.register(r'emergency-reserve', EmergencyReserveViewSet)
ROUTER.register(r'protection-manager', ProtectionManagerViewSet)
ROUTER.register(r'reserve-in-lack', ReserveInLackViewSet)
ROUTER.register(r'actual-patrimony-succession',
                ActualPatrimonySuccessionViewSet)
ROUTER.register(r'independence-patrimony-succession',
                IndependencePatrimonySuccessionViewSet)
ROUTER.register(r'private-pension', PrivatePensionViewSet)
ROUTER.register(r'life-insurance', LifeInsuranceViewSet)

urlpatterns = ROUTER.urls
