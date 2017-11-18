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
    """
    retrieve:
        Return a goal instance.

    list:
        Return all goals, ordered by most recently joined.

    create:
        Create a new goal.

    delete:
        Remove an existing goal.

    partial_update:
        Update one or more fields on an existing goal.

    update:
        Update a goal.
    """

    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
   


class GoalTypeViewSet(viewsets.ModelViewSet):
    serializer_class = GoalTypeSerializer
    queryset = GoalType.objects.all()


class GoalManagerViewSet(viewsets.ModelViewSet):
    serializer_class = GoalManagerSerializer
    queryset = GoalManager.objects.all()
