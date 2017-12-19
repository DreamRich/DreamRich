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
ROUTER.register(r'emergency_reserve', EmergencyReserveViewSet)
ROUTER.register(r'protection_manager', ProtectionManagerViewSet)
ROUTER.register(r'reserve_lack', ReserveInLackViewSet)
ROUTER.register(r'actual_patrimony', ActualPatrimonySuccessionViewSet)
ROUTER.register(r'independence_patrimony',
        IndependencePatrimonySuccessionViewSet)
ROUTER.register(r'private_pension', PrivatePensionViewSet)
ROUTER.register(r'life_insurance', LifeInsuranceViewSet)

urlpatterns = ROUTER.urls
