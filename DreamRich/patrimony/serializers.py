from patrimony.models import (
    Patrimony,
    Active,
    Arrearage,
    RealEstate,
    CompanyParticipation,
    Equipment,
    LifeInsurance,
    Income,
)
from rest_framework import serializers


class PatrimonySerializer(serializers.ModelSerializer):

    class Meta:
        model = Patrimony
        fields = [
            'fgts',
            'id',
        ]


class ActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Active
        fields = [
            'name',
            'value',
        ]


class ArrearageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Arrearage
        fields = [
            'name',
            'value',
        ]


class RealEstateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RealEstate
        fields = [
            'name',
            'value',
            'salable',
        ]


class CompanyParticipationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyParticipation
        fields = [
            'name',
            'value',
        ]


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = [
            'name',
            'value',
        ]


class LifeInsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = LifeInsurance
        fields = [
            'name',
            'value',
        ]


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = [
            'source',
            'value_monthly',
            'thirteenth',
            'vacation',
        ]
