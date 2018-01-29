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
from dr_auth.permissions import GeneralPermissions


class GoalViewSet(viewsets.ModelViewSet):

    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    permission_classes = (GeneralPermissions,)


class GoalTypeViewSet(viewsets.ModelViewSet):

    serializer_class = GoalTypeSerializer
    queryset = GoalType.objects.all()
    permission_classes = (GeneralPermissions,)


class GoalManagerViewSet(viewsets.ModelViewSet):

    serializer_class = GoalManagerSerializer
    queryset = GoalManager.objects.all()
    permission_classes = (GeneralPermissions,)
