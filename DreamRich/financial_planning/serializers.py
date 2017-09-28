from financial_planning.models import RegularCost
from rest_framework import serializers


class RegularCostSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegularCost
        fields = [
            'home',
            'electricity_bill',
            'gym',
            'taxes',
            'car_gas',
            'insurance',
            'cellphone',
            'health_insurance',
            'supermarket',
            'housekeeper',
            'beauty',
            'internet',
            'netflix',
            'recreation',
            'meals',
            'appointments',
            'drugstore',
            'extras',
        ]
