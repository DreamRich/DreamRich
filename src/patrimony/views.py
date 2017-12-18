from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from patrimony.serializers import (
    PatrimonySerializer,
    ActiveSerializer,
    ActiveManagerSerializer,
    ActiveChartSerializer,
    ActiveTypeSerializer,
    ArrearageSerializer,
    RealEstateSerializer,
    CompanyParticipationSerializer,
    EquipmentSerializer,
    IncomeSerializer,
)

from patrimony.models import (
    Active,
    ActiveType,
    ActiveManager,
    Arrearage,
    CompanyParticipation,
    Equipment,
    Income,
    Patrimony,
    RealEstate,
)


class PatrimonyViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a patrimony instance.

    list:
        Return all patrimonies, ordered by most recently joined.

    create:
        Create a new regular patrimony.

    delete:
        Remove an existing regular patrimony.

    partial_update:
        Update one or more fields on an existing patrimony.

    update:
        Update a patrimony.
    """

    serializer_class = PatrimonySerializer
    queryset = Patrimony.objects.all()


class ActiveManagerViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a active manager instance.

    list:
        Return all active managers, ordered by most recently joined.

    create:
        Create a new regular active manager.

    delete:
        Remove an existing regular active manager.

    partial_update:
        Update one or more fields on an existing active manager.

    update:
        Update a active manager.
    """

    serializer_class = ActiveManagerSerializer
    queryset = ActiveManager.objects.all()


class ActiveChartDetailView(viewsets.ModelViewSet):
    """
    retrieve:
        Return a active chart instance.

    list:
        Return all active charts, ordered by most recently joined.

    create:
        Create a new regular active chart.

    delete:
        Remove an existing regular active chart.

    partial_update:
        Update one or more fields on an existing active chart.

    update:
        Update a active chart.
    """

    serializer_class = ActiveChartSerializer
    queryset = ActiveManager.objects.all()


class ActiveTypeViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a active type instance.

    list:
        Return all active types, ordered by most recently joined.

    create:
        Create a new regular active type.

    delete:
        Remove an existing regular active type.

    partial_update:
        Update one or more fields on an existing active type.

    update:
        Update a active type.
    """

    serializer_class = ActiveTypeSerializer
    queryset = ActiveType.objects.all()


class ActiveViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a active instance.

    list:
        Return all actives, ordered by most recently joined.

    create:
        Create a new regular active.

    delete:
        Remove an existing regular active.

    partial_update:
        Update one or more fields on an existing active.

    update:
        Update a active.
    """

    serializer_class = ActiveSerializer
    queryset = Active.objects.all()


class ArrearageViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a arrearage instance.

    list:
        Return all arrearages, ordered by most recently joined.

    create:
        Create a new regular arrearage.

    delete:
        Remove an existing regular arrearage.

    partial_update:
        Update one or more fields on an existing arrearage.

    update:
        Update a arrearage.
    """

    serializer_class = ArrearageSerializer
    queryset = Arrearage.objects.all()

    # pylint: disable=invalid-name, unused-argument, no-self-use
    @detail_route(methods=['get'])
    def list_calculator(self, request, pk=None):
        arrearage = Arrearage.objects.get(pk=pk)
        return Response(
            arrearage.calculate_arrearage()
        )

    @detail_route(methods=['get'])
    def patrimony_arrearage(self, request, pk=None):
        arrearages = Arrearage.objects.filter(patrimony_id=pk)

        list_arrearage = []
        for arrearage in arrearages:
            list_arrearage.append({
                'id': arrearage.id,
                'name': arrearage.name,
                'value': arrearage.value,
                'period': arrearage.period,
                'rate': arrearage.rate,
                'amortization_system': arrearage.amortization_system
            })
        return Response(list_arrearage)


class RealEstateViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a real estate instance.

    list:
        Return all real estates, ordered by most recently joined.

    create:
        Create a new regular real estate.

    delete:
        Remove an existing regular real estate.

    partial_update:
        Update one or more fields on an existing real estate.

    update:
        Update a real estate.
    """

    serializer_class = RealEstateSerializer
    queryset = RealEstate.objects.all()


class CompanyParticipationViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a company participation instance.

    list:
        Return all companies participations, ordered by most recently joined.

    create:
        Create a new regular company participation.

    delete:
        Remove an existing regular company participation.

    partial_update:
        Update one or more fields on an existing company participation.

    update:
        Update a company participation.
    """

    serializer_class = CompanyParticipationSerializer
    queryset = CompanyParticipation.objects.all()


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a equipament instance.

    list:
        Return all equipaments, ordered by most recently joined.

    create:
        Create a new regular equipament.

    delete:
        Remove an existing regular equipament.

    partial_update:
        Update one or more fields on an existing equipament.

    update:
        Update a equipament.
    """

    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()


class IncomeViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a income instance.

    list:
        Return all incomes, ordered by most recently joined.

    create:
        Create a new regular income.

    delete:
        Remove an existing regular income.

    partial_update:
        Update one or more fields on an existing income.

    update:
        Update a income.
    """

    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
