from financial_planning.models import (
    RegularCost, CostManager, CostType, FinancialPlanning
)
from rest_framework import serializers


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

    class Meta:
        model = FinancialPlanning
        fields = [
            'pk',
            'total_resource_for_annual_goals',
        ]
