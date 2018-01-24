from rest_framework import viewsets
from dr_auth.permissions import GeneralPermissions
from .models import (
    EmergencyReserve, ProtectionManager, ReserveInLack,
    ActualPatrimonySuccession, IndependencePatrimonySuccession,
    PrivatePension, LifeInsurance
)
from .serializers import (
    EmergencyReserveSerializer, ProtectionManagerSerializer,
    ReserveInLackSerializer,
    ActualPatrimonySuccessionSerializer,
    IndependencePatrimonySuccessionSerializer,
    PrivatePensionSerializer, LifeInsuranceSerializer
)


class EmergencyReserveViewSet(viewsets.ModelViewSet):

    queryset = EmergencyReserve.objects.all()
    serializer_class = EmergencyReserveSerializer
    permission_classes = (GeneralPermissions,)


class ProtectionManagerViewSet(viewsets.ModelViewSet):

    queryset = ProtectionManager.objects.all()
    serializer_class = ProtectionManagerSerializer
    permission_classes = (GeneralPermissions,)


class ReserveInLackViewSet(viewsets.ModelViewSet):

    queryset = ReserveInLack.objects.all()
    serializer_class = ReserveInLackSerializer
    permission_classes = (GeneralPermissions,)


class ActualPatrimonySuccessionViewSet(viewsets.ModelViewSet):

    queryset = ActualPatrimonySuccession.objects.all()
    serializer_class = ActualPatrimonySuccessionSerializer
    permission_classes = (GeneralPermissions,)


class IndependencePatrimonySuccessionViewSet(viewsets.ModelViewSet):

    queryset = IndependencePatrimonySuccession.objects.all()
    serializer_class = IndependencePatrimonySuccessionSerializer
    permission_classes = (GeneralPermissions,)


class PrivatePensionViewSet(viewsets.ModelViewSet):

    queryset = PrivatePension.objects.all()
    serializer_class = PrivatePensionSerializer
    permission_classes = (GeneralPermissions,)


class LifeInsuranceViewSet(viewsets.ModelViewSet):

    queryset = LifeInsurance.objects.all()
    serializer_class = LifeInsuranceSerializer
    permission_classes = (GeneralPermissions,)
