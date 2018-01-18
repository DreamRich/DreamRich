from rest_framework import serializers
from .models import (
    EmergencyReserve, ProtectionManager, ReserveInLack,
    ActualPatrimonySuccession, IndependencePatrimonySuccession,
    PrivatePension, LifeInsurance
)


class EmergencyReserveSerializer(serializers.ModelSerializer):

    cost_manager_id = serializers.IntegerField(write_only=True)
    patrimony_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EmergencyReserve

        fields = [
            'id',
            'month_of_protection',
            'cost_manager_id',
            'patrimony_id',
        ]


class ReserveInLackSerializer(serializers.ModelSerializer):

    protection_manager_id = serializers.IntegerField(write_only=True)

    class Meta:

        model = ReserveInLack

        fields = [
            'id',
            'value_0_to_24_month',
            'value_24_to_60_month',
            'value_60_to_120_month',
            'value_120_to_240_month',
            'protection_manager_id',
        ]


class PatrimonySuccessionSerializer(serializers.ModelSerializer):

    protection_manager_id = serializers.IntegerField(write_only=True)

    class Meta:

        fields = [
            'id',
            'itcmd_tax',
            'oab_tax',
            'other_taxes',
            'protection_manager_id',
        ]


class ActualPatrimonySuccessionSerializer(PatrimonySuccessionSerializer):

    class Meta:

        model = ActualPatrimonySuccession
        fields = PatrimonySuccessionSerializer.Meta.fields


class IndependencePatrimonySuccessionSerializer(serializers.ModelSerializer):

    class Meta:

        model = IndependencePatrimonySuccession
        fields = PatrimonySuccessionSerializer.Meta.fields


class PrivatePensionSerializer(serializers.ModelSerializer):

    protection_manager_id = serializers.IntegerField(write_only=True)

    class Meta:

        model = PrivatePension

        fields = [
            'id',
            'name',
            'value_annual',
            'accumulated',
            'rate',
            'protection_manager_id',
        ]


class LifeInsuranceSerializer(serializers.ModelSerializer):

    protection_manager_id = serializers.IntegerField(write_only=True)

    class Meta:

        model = LifeInsurance

        fields = [
            'id',
            'name',
            'value_to_recive',
            'value_to_pay_annual',
            'year_end',
            'redeemable',
            'actual',
            'has_year_end',
            'protection_manager_id',
        ]


class ProtectionManagerSerializer(serializers.ModelSerializer):

    financial_planning_id = serializers.IntegerField(write_only=True)
    reserve_in_lack = ReserveInLackSerializer(read_only=True)
    actual_patrimony_succession = ActualPatrimonySuccessionSerializer(
        read_only=True)
    future_patrimony_succession = IndependencePatrimonySuccessionSerializer(
        read_only=True)
    life_insurances = LifeInsuranceSerializer(many=True, read_only=True)
    private_pensions = PrivatePensionSerializer(many=True, read_only=True)

    class Meta:
        model = ProtectionManager
        fields = [
            'id',
            'financial_planning_id',
            'reserve_in_lack',
            'actual_patrimony_succession',
            'future_patrimony_succession',
            'life_insurances',
            'private_pensions',
        ]
