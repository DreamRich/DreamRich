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
from dr_auth.models_permissions import ClientsModelPermissions
from dr_auth.custom_permissions import ClientsCustomPermissions


class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (ClientsModelPermissions, ClientsCustomPermissions)


class ActiveClientViewSet(viewsets.ModelViewSet):

    serializer_class = ActiveClientSerializer
    queryset = ActiveClient.objects.all()
    permission_classes = (ClientsModelPermissions, ClientsCustomPermissions)


class AddressViewSet(viewsets.ModelViewSet):

    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = (ClientsModelPermissions, ClientsCustomPermissions)

    @list_route(methods=['get'])
    def type_of_address(self, unused_request):
        addresses = self.queryset.values('type_of_address').distinct()
        distinct_types = map(lambda x: x['type_of_address'], addresses)
        return Response(list(distinct_types), 200)


class StateViewSet(viewsets.ModelViewSet):

    serializer_class = StateSerializer
    queryset = State.objects.all()
    filter_fields = ('country_id', )
    permission_classes = (ClientsModelPermissions, ClientsCustomPermissions)

    def list(self, request):
        country_id = request.query_params.get('country_id', None)

        states = State.objects.filter(
                country_id=country_id
        ) if country_id else self.queryset


class CountryViewSet(viewsets.ModelViewSet):

    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = (ClientsModelPermissions, ClientsCustomPermissions)


class BankAccountViewSet(viewsets.ModelViewSet):

    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
    permission_classes = (ClientsModelPermissions, ClientsCustomPermissions)


class DependentViewSet(viewsets.ModelViewSet):

    serializer_class = DependentSerializer
    queryset = Dependent.objects.all()
    permission_classes = (ClientsModelPermissions, ClientsCustomPermissions)
