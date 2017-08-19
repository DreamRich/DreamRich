from rest_framework import serializers
from client.models import (
    Address,
    ActiveClient,
    BankAccount,
    State,
    Country,
    Dependent
)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            'city',
            'type_of_address',
            'neighborhood',
            'detail',
            'cep',
            'number',
            'complement'
        ]


class StateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)

    class Meta:
        model = State
        fields = ['name']


class CountrySerializer(serializers.ModelSerializer):
    state_addresses = StateSerializer(many=True)

    class Meta:
        model = Country
        fields = [
            'name',
            'state',
            'state_acronym'
        ]


class DependentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dependent
        fields = [
            'active_client',
            'birthday'
        ]


class BankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = [
            'agency',
            'account'
        ]


class ActiveClientSerializer(serializers.ModelSerializer):
    id_document = serializers.ImageField(read_only=True)
    proof_of_address = serializers.ImageField(read_only=True)
    dependents = DependentSerializer(many=True)
    client_addresses = AddressSerializer(many=True)
    bankAccount = BankAccountSerializer()

    class Meta:
        model = ActiveClient
        fields = [
            'name',
            'birthday',
            'profession',
            'cpf',
            'telephone',
            'email',
            'hometown',
            'id_document',
            'proof_of_address',
            'dependents',
            'client_addresses',
            'bankAccount'
        ]
