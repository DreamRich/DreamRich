from rest_framework import viewsets, generics
from financial_planning.serializers import (
    RegularCostSerializer,
    CostManagerSerializer,
    CostTypeSerializer,
    FinancialPlanningSerializer,
)
from financial_planning.models import (
    RegularCost,
    CostManager,
    CostType,
    FinancialPlanning,
)


class CostTypeViewList(generics.ListAPIView):
    serializer_class = CostTypeSerializer
    queryset = CostType.objects.all()


class RegularCostViewSet(viewsets.ModelViewSet):
    serializer_class = RegularCostSerializer
    queryset = RegularCost.objects.all()


class CostManagerViewSet(viewsets.ModelViewSet):
    serializer_class = CostManagerSerializer
    queryset = CostManager.objects.all()


class FinancialPlanningViewSet(viewsets.ModelViewSet):

    serializer_class = FinancialPlanningSerializer
    queryset = FinancialPlanning.objects.all()

