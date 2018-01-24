from rest_framework import serializers
from financial_planning.models import (
    RegularCost, CostManager,
    CostType, FinancialPlanning,
    FlowUnitChange, FinancialIndependence,
)
from patrimony.serializers import PatrimonySerializer
from goal.serializers import GoalManagerSerializer
from client.serializers import ActiveClientSerializer


class FinancialIndependenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialIndependence
        fields = [
            'pk',
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
            'pk',
            'annual_value',
            'year',
            'cost_manager_id',
            'incomes_id',
        ]


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
    active_client = ActiveClientSerializer(read_only=True)

    class Meta:
        model = FinancialPlanning
        fields = [
            'pk',
            'patrimony',
            'active_client',
            'financial_independence',
            'goal_manager',
            'cost_manager',
            'cdi',
            'ipca',
            'target_profitability',
            'year_init_to_end',
            'total_resource_for_annual_goals',
            'suggested_flow_patrimony',
            'actual_flow_patrimony'
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
