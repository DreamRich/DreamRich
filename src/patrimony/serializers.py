from patrimony.models import (
    Patrimony,
    ActiveType,
    ActiveManager,
    Active,
    Arrearage,
    ArrearageCalculator,
    RealEstate,
    CompanyParticipation,
    Equipment,
    Income,
)
from rest_framework import serializers


class ActiveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveType
        fields = ['id', 'name']


class ActiveSerializer(serializers.ModelSerializer):

    active_manager_id = serializers.IntegerField(write_only=True)
    active_type_id = serializers.IntegerField()
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
        ]


class ActiveChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveManager
        fields = [
            'active_type_chart',
        ]


class ArrearageCalculatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArrearageCalculator
        fields = [
            'calculate_arrearage',
        ]


class ArrearageSerializer(serializers.ModelSerializer):

    arrearage_calculator = ArrearageCalculatorSerializer(
        many=False,
        read_only=True
    )
    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Arrearage
        fields = [
            'id',
            'name',
            'patrimony_id',
            'value',
            'period',
            'rate',
            'amortization_system',
            'arrearage_calculator',
            'actual_period',
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


class IncomeSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Income
        fields = [
            'id',
            'source',
            'value_monthly',
            'thirteenth',
            'fourteenth',
            'vacation',
            'patrimony_id',
        ]


class PatrimonySerializer(serializers.ModelSerializer):

    activemanager = ActiveManagerSerializer(read_only=True)
    arrearages = ArrearageSerializer(read_only=True, many=True)
    realestates = RealEstateSerializer(read_only=True, many=True)
    companyparticipations = CompanyParticipationSerializer(many=True,
                                                           read_only=True)
    equipments = EquipmentSerializer(many=True, read_only=True)
    incomes = IncomeSerializer(many=True, read_only=True)

    class Meta:
        model = Patrimony
        fields = [
            'fgts',
            'id',
            'activemanager',
            'arrearages',
            'realestates',
            'companyparticipations',
            'equipments',
            'incomes',
        ]
