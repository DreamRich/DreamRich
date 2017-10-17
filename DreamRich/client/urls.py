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

app_name = 'client'  # pylint: disable=invalid-name

router = routers.DefaultRouter()  # pylint: disable=invalid-name
router.register(r'^active', ActiveClientViewSet)
router.register(r'^address', AddressViewSet)
router.register(r'^state', StateViewSet)
router.register(r'^country', CountryViewSet)
router.register(r'^bank-account', BankAccountViewSet)
router.register(r'^dependent', DependentViewSet)
router.register(r'', ClientViewSet)

urlpatterns = router.urls
