from rest_framework import routers
from goal.views import (GoalManagerViewSet, GoalTypeViewSet, GoalViewSet)

APP_NAME = 'goal'

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^goal_manager', GoalManagerViewSet)
ROUTER.register(r'^goal_type', GoalTypeViewSet)
ROUTER.register(r'^goal', GoalViewSet)

urlpatterns = ROUTER.urls
