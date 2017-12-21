from goal.models import GoalManager, GoalType, Goal
from rest_framework import serializers


class GoalTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalType
        fields = ['name', 'pk']


class GoalSerializer(serializers.ModelSerializer):

    goal_manager_id = serializers.IntegerField(write_only=True)
    goal_type = GoalTypeSerializer(read_only=True)
    goal_type_id = serializers.IntegerField()

    class Meta:
        model = Goal
        fields = [
            'pk',
            'value',
            'periodicity',
            'end_year',
            'init_year',
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
            'pk',
            'goals_flow_dic',
            'year_init_to_year_end',
            'goals',
        ]
