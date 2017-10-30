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
    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (ClientsPermission,)


class ActiveClientViewSet(viewsets.ModelViewSet):
    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = ActiveClientSerializer
    queryset = ActiveClient.objects.all()
    permission_classes = (ClientsPermission,)


class AddressViewSet(viewsets.ModelViewSet):
    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    @list_route(methods=['get'])
    def type_of_address(self, unused_request):
        addresses = self.queryset.values('type_of_address').distinct()
        mapped = map(lambda x: x['type_of_address'], addresses)
        return Response(list(mapped), 200)


class StateViewSet(viewsets.ModelViewSet):
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
    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()


class DependentViewSet(viewsets.ModelViewSet):
    required_permission = {'PUT': 'change_own_client_data',
                           'GET': 'see_own_client_data'}
    serializer_class = DependentSerializer
    queryset = Dependent.objects.all()
