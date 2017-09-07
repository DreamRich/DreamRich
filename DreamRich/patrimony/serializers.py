from patrimony.models import (
    Patrimony,
    Active,
    Arrearage,
    RealEstate,
    CompanyParticipation,
    Equipment,
    LifeInsurance,
    Income,
    Leftover,
    MovableProperty,
    RegularCost,
)
from rest_framework import serializers


class ActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Active
        fields = [
            'name',
            'value',
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


class RealEstateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RealEstate
        fields = [
            'name',
            'value',
            'salable',
        ]

class PatrimonySerializer(serializers.ModelSerializer):

    class Meta:
        model = Patrimony
        fields = [
            'fgts',
        ]
