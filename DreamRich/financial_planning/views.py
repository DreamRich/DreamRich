from financial_planning.serializers import (
    RegularCostSerializer,
)
from financial_planning.models import (
    RegularCost,
)


class RegularCostViewSet(viewsets.ModelViewSet):
    serializer_class = RegularCostSerializer
    queryset = RegularCost.objects.all()
