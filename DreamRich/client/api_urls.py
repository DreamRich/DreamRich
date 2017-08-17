from client.views import ClientViewSet
from django.conf.urls import url
from rest_framework import routers

app_name = 'client'

router = routers.DefaultRouter()
router.register(r'', ClientViewSet)

urlpatterns = router.urls
