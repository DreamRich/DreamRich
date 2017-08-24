from rest_framework import serializers
from client.models import (
    Address,
    Client,
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

    class Meta:
        model = State
        fields = [
            'name',
            'abbreviation'
        ]


class CountrySerializer(serializers.ModelSerializer):
    country_states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = [
            'name',
            'abbreviation',
            'country_states'
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


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'name',
            'birthday',
            'profession',
            'cpf',
            'telephone',
            'email',
            'hometown'
        ]


class ActiveClientSerializer(serializers.ModelSerializer):
    dependents = DependentSerializer(many=True)
    client_address = AddressSerializer(many=True)

    id_document = serializers.ImageField(read_only=True)
    proof_of_address = serializers.ImageField(read_only=True)
    client_bank_account = BankAccountSerializer()

    spouse = ClientSerializer()

    class Meta:

        model = ActiveClient
        fields = ClientSerializer.Meta.fields + [
            'client_address',
            'dependents',
            'id_document',
            'proof_of_address',
            'client_bank_account',
            'spouse'
        ]
