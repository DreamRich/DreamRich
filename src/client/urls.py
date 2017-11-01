from rest_framework import routers
from client.views import (
    ActiveClientViewSet,
    ClientViewSet,
    AddressViewSet,
    StateViewSet,
    CountryViewSet,
    BankAccountViewSet,
    DependentViewSet,
)

APP_NAME = 'client'

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^active', ActiveClientViewSet)
ROUTER.register(r'^address', AddressViewSet)
ROUTER.register(r'^state', StateViewSet)
ROUTER.register(r'^country', CountryViewSet)
ROUTER.register(r'^bank-account', BankAccountViewSet)
ROUTER.register(r'^dependent', DependentViewSet)
ROUTER.register(r'', ClientViewSet)

urlpatterns = ROUTER.urls
