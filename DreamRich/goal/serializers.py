from goal.models import GoalManager
from rest_framework import serializers


class GoalManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalManager
        fields = [
            'goals_flow_dic',
        ]
