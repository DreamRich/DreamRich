from patrimony.models import (
    Patrimony,
    ActiveType,
    ActiveManager,
    Active,
    Arrearage,
    RealState,
    CompanyParticipation,
    Equipment,
    Income,
)
from rest_framework import serializers


class ActiveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveType
        fields = ['pk', 'name']


class ActiveSerializer(serializers.ModelSerializer):

    active_manager_id = serializers.IntegerField(write_only=True)
    active_type_id = serializers.IntegerField()
    active_type = ActiveTypeSerializer(read_only=True)

    class Meta:
        model = Active
        fields = [
            'pk',
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
            'pk',
            'patrimony_id',
            'actives',
        ]


class ActiveChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveManager
        fields = [
            'active_type_chart',
            'active_chart_dataset',
        ]


class ArrearageSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Arrearage
        fields = [
            'pk',
            'name',
            'patrimony_id',
            'value',
            'period',
            'rate',
            'amortization_system',
            'actual_period',
            'calculate_arrearage',
        ]


class RealStateSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RealState
        fields = [
            'pk',
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
            'pk',
            'name',
            'value',
            'patrimony_id',
        ]


class EquipmentSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Equipment
        fields = [
            'pk',
            'name',
            'value',
            'patrimony_id',
        ]


class IncomeSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Income
        fields = [
            'pk',
            'source',
            'value_monthly',
            'thirteenth',
            'fourteenth',
            'vacation',
            'patrimony_id',
        ]


class PatrimonySerializer(serializers.ModelSerializer):

    active_manager = ActiveManagerSerializer(read_only=True)
    arrearages = ArrearageSerializer(read_only=True, many=True)
    real_estates = RealStateSerializer(read_only=True, many=True)
    company_participations = CompanyParticipationSerializer(many=True,
                                                            read_only=True)
    equipments = EquipmentSerializer(many=True, read_only=True)
    incomes = IncomeSerializer(many=True, read_only=True)

    class Meta:
        model = Patrimony
        fields = [
            'pk',
            'fgts',
            'active_manager',
            'arrearages',
            'real_estates',
            'company_participations',
            'equipments',
            'incomes',
        ]
