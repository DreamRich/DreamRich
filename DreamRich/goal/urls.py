from rest_framework import routers
from goal.views import * 

app_name = 'goal' # pylint: disable=invalid-name

router = routers.DefaultRouter() # pylint: disable=invalid-name
router.register(r'^goal_manager', GoalManagerViewSet)
router.register(r'^goal_type', GoalTypeViewSet)
router.register(r'^goal', GoalViewSet)
urlpatterns = router.urls
