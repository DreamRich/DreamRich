from patrimony.models import (
    Patrimony,
    ActiveType,
    ActiveManager,
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


class ActiveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveType
        fields = ['id', 'name']


class ActiveSerializer(serializers.ModelSerializer):

    active_manager_id = serializers.IntegerField(write_only=True)
    active_type_id = serializers.IntegerField(write_only=True)
    active_type = ActiveTypeSerializer(read_only=True)

    class Meta:
        model = Active
        fields = [
            'id',
            'name',
            'value',
            'rate',
            'equivalent_rate',
            'active_manager_id',
            'active_type_id',
            'active_type',
        ]


class ActiveManagerSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)
    actives = ActiveSerializer(many=True, read_only=True)

    class Meta:
        model = ActiveManager
        fields = [
            'id',
            'patrimony_id',
            'actives',
            'active_type_labels',
            'active_type_data',
        ]


class ArrearageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Arrearage
        fields = [
            'name',
            'value',
            'period',
            'rate',
            'amortization_system',
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
