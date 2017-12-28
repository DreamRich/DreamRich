from rest_framework import viewsets
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
    """
    retrieve:
        Return a emergency reserve instance.

    list:
        Return all emergency reserves, ordered by most recently joined.

    create:
        Create a new regular emergency reserve.

    delete:
        Remove an existing regular emergency reserve.

    partial_update:
        Update one or more fields on an existing emergency reserve.

    update:
        Update a emergency reserve.
    """

    queryset = EmergencyReserve.objects.all()
    serializer_class = EmergencyReserveSerializer
    filter_fields = ('cost_manager_id', 'patrimony_id')


class ProtectionManagerViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a protection manager instance.

    list:
        Return all protection managers, ordered by most recently joined.

    create:
        Create a new regular protection manager.

    delete:
        Remove an existing regular protection manager.

    partial_update:
        Update one or more fields on an existing protection manager.

    update:
        Update a protection manager.
    """

    queryset = ProtectionManager.objects.all()
    serializer_class = ProtectionManagerSerializer


class ReserveInLackViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a reserve in lack instance.

    list:
        Return all reserve in lacks, ordered by most recently joined.

    create:
        Create a new regular reserve in lack.

    delete:
        Remove an existing regular reserve in lack.

    partial_update:
        Update one or more fields on an existing reserve in lack.

    update:
        Update a reserve in lack.
    """

    queryset = ReserveInLack.objects.all()
    serializer_class = ReserveInLackSerializer


class ActualPatrimonySuccessionViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a actual patrimony instance.

    list:
        Return all actual patrimonys, ordered by most recently joined.

    create:
        Create a new regular actual patrimony.

    delete:
        Remove an existing regular actual patrimony.

    partial_update:
        Update one or more fields on an existing actual patrimony.

    update:
        Update a actual patrimony.
    """

    queryset = ActualPatrimonySuccession.objects.all()
    serializer_class = ActualPatrimonySuccessionSerializer


class IndependencePatrimonySuccessionViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a furute patrimony instance.

    list:
        Return all furute patrimonys, ordered by most recently joined.

    create:
        Create a new regular furute patrimony.

    delete:
        Remove an existing regular furute patrimony.

    partial_update:
        Update one or more fields on an existing furute patrimony.

    update:
        Update a furute patrimony.
    """

    queryset = IndependencePatrimonySuccession.objects.all()
    serializer_class = IndependencePatrimonySuccessionSerializer


class PrivatePensionViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a private pension instance.

    list:
        Return all private pensions, ordered by most recently joined.

    create:
        Create a new regular private pension.

    delete:
        Remove an existing regular private pension.

    partial_update:
        Update one or more fields on an existing private pension.

    update:
        Update a private pension.
    """

    queryset = PrivatePension.objects.all()
    serializer_class = PrivatePensionSerializer


class LifeInsuranceViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a life insurance instance.

    list:
        Return all life insurances, ordered by most recently joined.

    create:
        Create a new regular life insurance.

    delete:
        Remove an existing regular life insurance.

    partial_update:
        Update one or more fields on an existing life insurance.

    update:
        Update a life insurance.
    """

    queryset = LifeInsurance.objects.all()
    serializer_class = LifeInsuranceSerializer
