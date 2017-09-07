from rest_framework import routers
from patrimony.views import PatrimonyViewSet

app_name = 'patrimony'

router = routers.DefaultRouter()
router.register('', PatrimonyViewSet)

urlpatterns = router.urls
