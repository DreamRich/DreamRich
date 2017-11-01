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


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = [
            'id',
            'name',
            'abbreviation',
            'country_id'
        ]


class CountrySerializer(serializers.ModelSerializer):
    country_states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'abbreviation',
            'country_states'
        ]


class AddressSerializer(serializers.ModelSerializer):

    state_id = serializers.IntegerField(write_only=True)
    active_client_id = serializers.IntegerField(write_only=True)
    state = StateSerializer(read_only=True)

    class Meta:
        model = Address
        fields = [
            'id',
            'city',
            'type_of_address',
            'neighborhood',
            'detail',
            'cep',
            'number',
            'complement',
            'state_id',
            'active_client_id',
            'state',
        ]


class DependentSerializer(serializers.ModelSerializer):

    active_client_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Dependent
        fields = [
            'id',
            'active_client_id',
            'birthday',
            'name',
            'surname'
        ]


class BankAccountSerializer(serializers.ModelSerializer):

    active_client_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BankAccount
        fields = [
            'id',
            'agency',
            'account',
            'active_client_id'
        ]


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id',
            'name',
            'surname',
            'birthday',
            'profession',
            'cpf',
            'telephone',
            'hometown'
        ]


class ActiveClientSerializer(serializers.ModelSerializer):
    dependents = DependentSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)
    spouse = ClientSerializer(read_only=True)
    bank_account = BankAccountSerializer(read_only=True)

    id_document = serializers.ImageField(read_only=True)
    proof_of_address = serializers.ImageField(read_only=True)

    class Meta:

        model = ActiveClient
        fields = ClientSerializer.Meta.fields + [
            'id',
            'addresses',
            'dependents',
            'id_document',
            'proof_of_address',
            'bank_account',
            'spouse',
            'email',
            'birthday',
        ]
