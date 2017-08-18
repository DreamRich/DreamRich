from django.conf.urls import url
from rest_framework import routers
from client.views import ActiveClientViewSet

app_name = 'client'

router = routers.DefaultRouter()
router.register(r'', ActiveClientViewSet)

urlpatterns = router.urls
