from rest_framework import routers
from goal.views import GoalManagerViewSet

app_name = 'goal'

router = routers.DefaultRouter()
router.register(r'^dic', GoalManagerViewSet)

urlpatterns = router.urls
