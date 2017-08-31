from employee.models import Employee, FinancialAdviser
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            'name',
            'surname',
            'cpf',
            'email',
        ]


class FinancialAdviserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialAdviser
        fields = [
            'name',
            'surname',
            'cpf',
            'email',
        ]
