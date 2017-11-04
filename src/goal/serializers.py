from goal.models import GoalManager, GoalType, Goal
from rest_framework import serializers


class GoalTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalType
        fields = ['name', 'id']


class GoalSerializer(serializers.ModelSerializer):

    goal_manager_id = serializers.IntegerField(write_only=True)
    goal_type = GoalTypeSerializer(read_only=True)
    goal_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Goal
        fields = [
            'id',
            'value',
            'periodicity',
            'year_end',
            'year_init',
            'has_end_date',
            'goal_type_id',
            'goal_type',
            'goal_manager_id'
        ]


class GoalManagerSerializer(serializers.ModelSerializer):

    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = GoalManager
        fields = [
            'id',
            'goals_flow_dic',
            'year_init_to_year_end',
            'goals',
        ]
