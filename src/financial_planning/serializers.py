from rest_framework import serializers
from financial_planning.models import (
    RegularCost,
    CostManager,
    CostType,
    FinancialPlanning
)
from patrimony.serializers import PatrimonySerializer
from goal.serializers import GoalManagerSerializer


class CostTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CostType
        fields = [
            'pk',
            'name'
        ]


class RegularCostSerializer(serializers.ModelSerializer):

    cost_type_id = serializers.IntegerField()
    cost_manager_id = serializers.IntegerField(write_only=True)
    cost_type = CostTypeSerializer(read_only=True)

    class Meta:
        model = RegularCost
        fields = [
            'pk',
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
            'pk',
            'regular_costs',
            'total_cost',
        ]


class FinancialPlanningSerializer(serializers.ModelSerializer):

    patrimony = PatrimonySerializer(read_only=True)
    goal_manager = GoalManagerSerializer(read_only=True)
    cost_manager = CostManagerSerializer(read_only=True)

    class Meta:
        model = FinancialPlanning
        fields = [
            'pk',
            'active_client_id',
            'patrimony',
            'financial_independence',
            'goal_manager',
            'cost_manager',
            'cdi',
            'ipca',
            'target_profitability',
        ]
