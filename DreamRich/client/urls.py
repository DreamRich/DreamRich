from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from client.views import AuthView
from client.views import (
    ActiveClientViewSet,
    ClientViewSet,
    AddressViewSet,
    StateViewSet,
    CountryViewSet,
    BankAccountViewSet
)

app_name = 'client'
urlpatterns = [
    url(r'^auth/$', obtain_jwt_token),
    url(r'^auth/password/', AuthView.as_view())
]

router = routers.DefaultRouter()
router.register(r'^active', ActiveClientViewSet)
router.register(r'^address', AddressViewSet)
router.register(r'^state', StateViewSet)
router.register(r'^country', CountryViewSet)
router.register(r'^bank-account', BankAccountViewSet)
router.register(r'', ClientViewSet)

urlpatterns += router.urls
