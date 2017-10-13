from rest_framework import viewsets
from financial_planning.serializers import (
    RegularCostSerializer,
    CostManagerSerializer
)
from financial_planning.models import (
    RegularCost,
    CostManager
)


class RegularCostViewSet(viewsets.ModelViewSet):
    serializer_class = RegularCostSerializer
    queryset = RegularCost.objects.all()


class CostManagerViewSet(viewsets.ModelViewSet):
    serializer_class = CostManagerSerializer
    queryset = CostManager.objects.all()
