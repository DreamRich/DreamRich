from dr_auth.permissions import ClientsPermission
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import generics
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
        Return a client instance.\
        Permissions: see_own_client_data

    list:
        Return all clients, ordered by most recently joined.\
        Permissions: see_own_client_data

    create:
        Create a new client.\
        Permissions: change_own_client_data

    delete:
        Remove an existing client.

    partial_update:
        Update one or more fields on an existing client.\
        Permissions: change_own_client_data

    update:
        Update a client.\
        Permissions: change_own_client_data
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (ClientsPermission,)


class ActiveClientViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a active client instance.\
        Permissions: see_own_client_data

    list:
        Return all active clients, ordered by most recently joined.\
        Permissions: see_own_client_data

    create:
        Create a new active client.\
        Permissions: change_own_client_data

    delete:
        Remove an existing active client.

    partial_update:
        Update one or more fields on an existing active client.\
        Permissions: change_own_client_data

    update:
        Update a active client.\
        Permissions: change_own_client_data
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = ActiveClientSerializer
    queryset = ActiveClient.objects.all()
    permission_classes = (ClientsPermission,)


class AddressViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a address instance.\
        Permissions: see_own_client_data


    list:
        Return all addresses, ordered by most recently joined.\
        Permissions: see_own_client_data


    create:
        Create a new address.\
        Permissions: change_own_client_data

    delete:
        Remove an existing address.

    partial_update:
        Update one or more fields on an existing address.\
        Permissions: change_own_client_data

    update:
        Update a address.\
        Permissions: change_own_client_data
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    @list_route(methods=['get'])
    def type_of_address(self, unused_request):
        """
            Return a type of address instance.\
            Permissions: see_own_client_data
        """
        addresses = self.queryset.values('type_of_address').distinct()
        mapped = map(lambda x: x['type_of_address'], addresses)
        return Response(list(mapped), 200)


class StateViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a state instance.\
        Permissions: see_own_client_data

    list:
        Return all states, ordered by most recently joined.\
        Permissions: see_own_client_data

    create:
        Create a new state.\
        Permissions: change_own_client_data

    delete:
        Remove an existing state.

    partial_update:
        Update one or more fields on an existing state.\
        Permissions: change_own_client_data

    update:
        Update a state.\
        Permissions: change_own_client_data
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = StateSerializer
    queryset = State.objects.all()
    filter_fields = ('country_id', )


class CountryViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a country instance.\
        Permissions: see_own_client_data

    list:
        Return all countries, ordered by most recently joined.\
        Permissions: see_own_client_data

    create:
        Create a new country.\
        Permissions: change_own_client_data

    delete:
        Remove an existing country.

    partial_update:
        Update one or more fields on an existing country.\
        Permissions: change_own_client_data

    update:
        Update a country.\
        Permissions: change_own_client_data
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a bank account instance.\
        Permissions: see_own_client_data

    list:
        Return all bank accounts, ordered by most recently joined.\
        Permissions: see_own_client_data

    create:
        Create a new bank account.\
        Permissions: change_own_client_data

    delete:
        Remove an existing bank account.

    partial_update:
        Update one or more fields on an existing bank account.\
        Permissions: change_own_client_data

    update:
        Update a bank account.\
        Permissions: change_own_client_data
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()


class DependentViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a dependent instance.\
        Permissions: see_own_client_data

    list:
        Return all dependents, ordered by most recently joined.\
        Permissions: see_own_client_data

    create:
        Create a new dependent.\
        Permissions: change_own_client_data

    delete:
        Remove an existing dependent.

    partial_update:
        Update one or more fields on an existing dependent.\
        Permissions: change_own_client_data

    update:
        Update a dependent.\
        Permissions: change_own_client_data
    """

    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = DependentSerializer
    queryset = Dependent.objects.all()
