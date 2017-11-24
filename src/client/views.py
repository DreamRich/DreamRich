from dr_auth.permissions import ClientsPermission
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

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
    """
    retrieve:
        Return a client instance.

    list:
        Return all clients, ordered by most recently joined.

    create:
        Create a new client.

    delete:
        Remove an existing client.

    partial_update:
        Update one or more fields on an existing client.

    update:
        Update a client.
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (ClientsPermission,)


class ActiveClientViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a active client instance.

    list:
        Return all active clients, ordered by most recently joined.

    create:
        Create a new active client.

    delete:
        Remove an existing active client.

    partial_update:
        Update one or more fields on an existing active client.

    update:
        Update a active client.
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = ActiveClientSerializer
    queryset = ActiveClient.objects.all()
    permission_classes = (ClientsPermission,)


class AddressViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a address instance.

    list:
        Return all addresses, ordered by most recently joined.

    create:
        Create a new address.

    delete:
        Remove an existing address.

    partial_update:
        Update one or more fields on an existing address.

    update:
        Update a address.
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    @list_route(methods=['get'])
    def type_of_address(self, unused_request):
        """
            Return a type of address instance.
        """ 
           
        addresses = self.queryset.values('type_of_address').distinct()
        mapped = map(lambda x: x['type_of_address'], addresses)
        return Response(list(mapped), 200)


class StateViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a state instance.

    list:
        Return all states, ordered by most recently joined.

    create:
        Create a new state.

    delete:
        Remove an existing state.

    partial_update:
        Update one or more fields on an existing state.

    update:
        Update a state.
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = StateSerializer
    queryset = State.objects.all()

    def list(self, request):
        country_id = request.GET.get('country_id')

        if country_id:
            states = State.objects.filter(country_id=country_id)
        else:
            states = self.queryset

        serializer = StateSerializer(states, many=True)

        return Response(serializer.data)


class CountryViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a country instance.

    list:
        Return all countries, ordered by most recently joined.

    create:
        Create a new country.

    delete:
        Remove an existing country.

    partial_update:
        Update one or more fields on an existing country.

    update:
        Update a country.
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a bank account instance.

    list:
        Return all bank accounts, ordered by most recently joined.

    create:
        Create a new bank account.

    delete:
        Remove an existing bank account.

    partial_update:
        Update one or more fields on an existing bank account.

    update:
        Update a bank account.
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()


class DependentViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a dependent instance.

    list:
        Return all dependents, ordered by most recently joined.

    create:
        Create a new dependent .

    delete:
        Remove an existing dependent .

    partial_update:
        Update one or more fields on an existing dependent .

    update:
        Update a dependent .
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = DependentSerializer
    queryset = Dependent.objects.all()
