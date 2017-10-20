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

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RealEstate
        fields = [
            'id',
            'name',
            'value',
            'salable',
            'patrimony_id',
        ]


class CompanyParticipationSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CompanyParticipation
        fields = [
            'id',
            'name',
            'value',
            'patrimony_id',
        ]


class EquipmentSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Equipment
        fields = [
            'id',
            'name',
            'value',
            'patrimony_id',
        ]


class LifeInsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = LifeInsurance
        fields = [
            'name',
            'value',
        ]


class IncomeSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Income
        fields = [
            'id',
            'source',
            'value_monthly',
            'thirteenth',
            'vacation',
            'patrimony_id',
        ]
