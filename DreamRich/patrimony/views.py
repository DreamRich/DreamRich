from rest_framework import viewsets
from patrimony.serializers import (
    PatrimonySerializer,
    ActiveSerializer,
    ArrearageSerializer,
    RealEstateSerializer,
    CompanyParticipationSerializer,
    EquipmentSerializer,
    LifeInsuranceSerializer,
    IncomeSerializer,
    RegularCostSerializer,
)

from patrimony.models import (
    Patrimony,
    Active,
    Arrearage,
    RealEstate,
    CompanyParticipation,
    Equipment,
    LifeInsurance,
    Income,
    RegularCost,
)


class PatrimonyViewSet(viewsets.ModelViewSet):
    serializer_class = PatrimonySerializer
    queryset = Patrimony.objects.all()


class ActiveViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveSerializer
    queryset = Active.objects.all()


class ArrearageViewSet(viewsets.ModelViewSet):
    serializer_class = ArrearageSerializer
    queryset = Arrearage.objects.all()


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


class RegularCostViewSet(viewsets.ModelViewSet):
    serializer_class = RegularCostSerializer
    queryset = RegularCost.objects.all()
