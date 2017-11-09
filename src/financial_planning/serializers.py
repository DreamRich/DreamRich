from rest_framework import serializers
from financial_planning.models import (
    RegularCost,
    CostManager,
    CostType,
    FinancialPlanning
)


class CostTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CostType
        fields = [
            'id',
            'name'
        ]


class RegularCostSerializer(serializers.ModelSerializer):

    cost_type_id = serializers.IntegerField(write_only=True)
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

    class Meta:
        model = FinancialPlanning
        fields = [
            'pk',
            'active_client_id',
            'patrimony_id',
            'financial_independence_id',
            'goal_manager_id',
            'cost_manager_id',
            'cdi',
            'ipca',
            'target_profitability',
        ]
