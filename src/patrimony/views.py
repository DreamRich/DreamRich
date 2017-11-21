from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.views.generic.detail import DetailView
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
    LifeInsuranceSerializer,
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
    LifeInsurance,
    Patrimony,
    RealEstate,
)


class PatrimonyViewSet(viewsets.ModelViewSet):
    serializer_class = PatrimonySerializer
    queryset = Patrimony.objects.all()


class ActiveManagerViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveManagerSerializer
    queryset = ActiveManager.objects.all()


class ActiveChartDetailView(viewsets.ModelViewSet):
    serializer_class = ActiveChartSerializer
    queryset = ActiveManager.objects.all()


class ActiveTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveTypeSerializer
    queryset = ActiveType.objects.all()


class ActiveViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveSerializer
    queryset = Active.objects.all()


class ArrearageViewSet(viewsets.ModelViewSet):
    serializer_class = ArrearageSerializer
    queryset = Arrearage.objects.all()

    # pylint: disable=invalid-name, unused-argument, no-self-use
    @detail_route(methods=['get'])
    def list_calculator(self, request, pk=None):
        arrearage = Arrearage.objects.get(pk=pk)
        return Response(
            arrearage.arrearage_calculator.calculate_arrearage
        )


class RealEstateViewSet(viewsets.ModelViewSet):
    serializer_class = RealEstateSerializer
    queryset = RealEstate.objects.all()


class CompanyParticipationViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyParticipationSerializer
    queryset = CompanyParticipation.objects.all()


class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()


class LifeInsuranceViewSet(viewsets.ModelViewSet):
    serializer_class = LifeInsuranceSerializer
    queryset = LifeInsurance.objects.all()


class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
