from rest_framework import routers
from goal.views import GoalManagerViewSet

app_name = 'goal' # pylint: disable=invalid-name

router = routers.DefaultRouter() # pylint: disable=invalid-name
router.register(r'^dic', GoalManagerViewSet)

urlpatterns = router.urls
