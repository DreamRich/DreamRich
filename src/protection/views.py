from rest_framework import viewsets
from dr_auth.models_permissions import GeneralModelPermissions
from dr_auth.custom_permissions import GeneralCustomPermissions
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
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class ProtectionManagerViewSet(viewsets.ModelViewSet):

    queryset = ProtectionManager.objects.all()
    serializer_class = ProtectionManagerSerializer
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class ReserveInLackViewSet(viewsets.ModelViewSet):

    queryset = ReserveInLack.objects.all()
    serializer_class = ReserveInLackSerializer
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class ActualPatrimonySuccessionViewSet(viewsets.ModelViewSet):

    queryset = ActualPatrimonySuccession.objects.all()
    serializer_class = ActualPatrimonySuccessionSerializer
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class IndependencePatrimonySuccessionViewSet(viewsets.ModelViewSet):

    queryset = IndependencePatrimonySuccession.objects.all()
    serializer_class = IndependencePatrimonySuccessionSerializer
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class PrivatePensionViewSet(viewsets.ModelViewSet):

    queryset = PrivatePension.objects.all()
    serializer_class = PrivatePensionSerializer
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class LifeInsuranceViewSet(viewsets.ModelViewSet):

    queryset = LifeInsurance.objects.all()
    serializer_class = LifeInsuranceSerializer
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)
