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
    """
    retrieve:
        Return a goal type instance.

    list:
        Return all goals type, ordered by most recently joined.

    create:
        Create a new goal type.

    delete:
        Remove an existing goal type.

    partial_update:
        Update one or more fields on an existing goal type.

    update:
        Update a goal type.
    """

    serializer_class = GoalTypeSerializer
    queryset = GoalType.objects.all()


class GoalManagerViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a goal manager instance.

    list:
        Return all goals manager, ordered by most recently joined.

    create:
        Create a new goal manager.

    delete:
        Remove an existing goal manager.

    partial_update:
        Update one or more fields on an existing goal manager.

    update:
        Update a goal manager.
    """

    serializer_class = GoalManagerSerializer
    queryset = GoalManager.objects.all()
