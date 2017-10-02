from rest_framework import viewsets
from client.serializers import (
    ClientSerializer,
    ActiveClientSerializer,
    AddressSerializer,
    StateSerializer,
    CountrySerializer,
    BankAccountSerializer,
    DependentSerializer
)
from client.models import (
    Client,
    ActiveClient,
    Address,
    State,
    Country,
    BankAccount,
    Dependent
)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ActiveClientViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveClientSerializer
    queryset = ActiveClient.objects.all()


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class StateViewSet(viewsets.ModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()

class DependentViewSet(viewsets.ModelViewSet):
    serializer_class = DependentSerializer
    queryset = Dependent.objects.all()
