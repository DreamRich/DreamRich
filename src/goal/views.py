from rest_framework import viewsets
from goal.serializers import (
    GoalSerializer,
    GoalTypeSerializer,
    GoalManagerSerializer,
)

from goal.models import (
    Goal,
    GoalType,
    GoalManager,
)


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()


class GoalTypeViewSet(viewsets.ModelViewSet):
    serializer_class = GoalTypeSerializer
    queryset = GoalType.objects.all()


class GoalManagerViewSet(viewsets.ModelViewSet):
    serializer_class = GoalManagerSerializer
    queryset = GoalManager.objects.all()
