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
from dr_auth.permissions import (
    GeneralModelPermissions,
    GeneralCustomPermissions
)


class GoalViewSet(viewsets.ModelViewSet):

    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class GoalTypeViewSet(viewsets.ModelViewSet):

    serializer_class = GoalTypeSerializer
    queryset = GoalType.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class GoalManagerViewSet(viewsets.ModelViewSet):

    serializer_class = GoalManagerSerializer
    queryset = GoalManager.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)
