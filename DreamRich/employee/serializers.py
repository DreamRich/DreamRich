from employee.models import Employee, FinancialAdviser
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'cpf',
            'email',
        ]


class FinancialAdviserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialAdviser
        fields = [
            'id',
            'first_name',
            'last_name',
            'cpf',
            'email',
        ]
