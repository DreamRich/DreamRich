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
    RealStateSerializer,
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
    RealState,
)
from dr_auth.permissions import GeneralPermissions


class PatrimonyViewSet(viewsets.ModelViewSet):

    serializer_class = PatrimonySerializer
    queryset = Patrimony.objects.all()
    permission_classes = (GeneralPermissions,)


class ActiveManagerViewSet(viewsets.ModelViewSet):

    serializer_class = ActiveManagerSerializer
    queryset = ActiveManager.objects.all()
    permission_classes = (GeneralPermissions,)


class ActiveChartDetailView(viewsets.ModelViewSet):

    serializer_class = ActiveChartSerializer
    queryset = ActiveManager.objects.all()
    permission_classes = (GeneralPermissions,)


class ActiveTypeViewSet(viewsets.ModelViewSet):

    serializer_class = ActiveTypeSerializer
    queryset = ActiveType.objects.all()
    permission_classes = (GeneralPermissions,)


class ActiveViewSet(viewsets.ModelViewSet):

    serializer_class = ActiveSerializer
    queryset = Active.objects.all()
    permission_classes = (GeneralPermissions,)


class ArrearageViewSet(viewsets.ModelViewSet):

    serializer_class = ArrearageSerializer
    queryset = Arrearage.objects.all()
    permission_classes = (GeneralPermissions,)

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


class RealStateViewSet(viewsets.ModelViewSet):

    serializer_class = RealStateSerializer
    queryset = RealState.objects.all()
    permission_classes = (GeneralPermissions,)


class CompanyParticipationViewSet(viewsets.ModelViewSet):

    serializer_class = CompanyParticipationSerializer
    queryset = CompanyParticipation.objects.all()
    permission_classes = (GeneralPermissions,)


class EquipmentViewSet(viewsets.ModelViewSet):

    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()
    permission_classes = (GeneralPermissions,)


class IncomeViewSet(viewsets.ModelViewSet):

    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (GeneralPermissions,)
