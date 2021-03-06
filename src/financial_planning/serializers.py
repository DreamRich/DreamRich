from rest_framework import serializers
from financial_planning.models import (
    RegularCost, CostManager,
    CostType, FinancialPlanning,
    FlowUnitChange, FinancialIndependence,
)


class FinancialIndependenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialIndependence
        fields = [
            'id',
            'age',
            'duration_of_usufruct',
            'rate',
            'remain_patrimony',
        ]


class FlowUnitChangeSerializer(serializers.ModelSerializer):

    cost_manager_id = serializers.IntegerField(required=False, write_only=True)
    incomes_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = FlowUnitChange
        fields = [
            'id',
            'annual_value',
            'year',
            'cost_manager_id',
            'incomes_id',
        ]


class CostTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CostType
        fields = [
            'id',
            'name'
        ]


class RegularCostSerializer(serializers.ModelSerializer):

    cost_type_id = serializers.IntegerField()
    cost_manager_id = serializers.IntegerField(write_only=True)
    cost_type = CostTypeSerializer(read_only=True)

    class Meta:
        model = RegularCost
        fields = [
            'id',
            'cost_type_id',
            'cost_manager_id',
            'value',
            'cost_type',
        ]


class CostManagerSerializer(serializers.ModelSerializer):

    regular_costs = RegularCostSerializer(many=True, read_only=True)
    total_cost = serializers.IntegerField(read_only=True)

    class Meta:
        model = CostManager
        fields = [
            'id',
            'regular_costs',
            'total_cost',
        ]


class FinancialPlanningSerializer(serializers.ModelSerializer):

    patrimony_id = serializers.IntegerField(required=False, allow_null=True)
    goal_manager_id = serializers.IntegerField(required=False, allow_null=True)
    cost_manager_id = serializers.IntegerField(required=False, allow_null=True)
    protection_manager = serializers.PrimaryKeyRelatedField(read_only=True)
    financial_independence_id = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = FinancialPlanning
        fields = [
            'pk',
            'active_client_id',
            'patrimony_id',
            'financial_independence_id',
            'goal_manager_id',
            'cost_manager_id',
            'protection_manager',
            'cdi',
            'ipca',
            'target_profitability',
        ]


class FinancialPlanningFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialPlanning
        fields = [
            'pk',
            'actual_flow_patrimony',
            'suggested_flow_patrimony',
            'year_init_to_end',
        ]
        read_only_fields = fields
