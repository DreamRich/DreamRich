from rest_framework import viewsets
from goal.serializers import (
    GoalManagerSerializer,
)
from goal.models import (
    GoalManager,
)


class GoalManagerViewSet(viewsets.ModelViewSet):
    serializer_class = GoalManagerSerializer
    queryset = GoalManager.objects.all()
