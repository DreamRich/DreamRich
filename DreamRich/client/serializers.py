from rest_framework import serializers
from client.models import (
    Address,
    BankAccount,
    Client,
    Dependent
)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            'cep',
            'number',
            'complement'
        ]


class DependentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dependent
        fields = [
            'client',
            'birthday'
        ]


class ClientSerializer(serializers.ModelSerializer):
    id_document = serializers.ImageField(read_only=True)
    proof_of_address = serializers.ImageField(read_only=True)
    dependents = DependentSerializer(many=True)

    class Meta:
        model = Client
        fields = [
            'name',
            'id_document',
            'proof_of_address',
            'birthday',
            'profession',
            'cpf',
            'telephone',
            'email',
            'address',
            'dependents',
            'hometown'
        ]


class BankAcoountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = [
            'client',
            'agency',
            'account'
        ]
