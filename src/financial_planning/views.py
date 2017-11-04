from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route
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
from employee.models import FinancialAdviser


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

    @detail_route(methods=['get'])
    # pylint: disable=invalid-name, no-self-use
    def respective_clients(self, request, pk=None):
        current_financial_adviser = FinancialAdviser.objects.filter(
            id=request.user.id).get()
        clients_ids_list = []
        # fp = Financial Planning and gm = Goal Manager
        fp_and_gm_pks = {}
        clients_ids = current_financial_adviser.clients.all().values('id')
        for ids in clients_ids:
            clients_ids_list.append(list(ids.values())[0])

        if int(pk) in clients_ids_list:
            try:
                financial_adviser_clients = current_financial_adviser.clients
                financial_planning_pk = financial_adviser_clients.filter(
                    id=pk).get().financialplanning.pk
                goal_manager_pk = current_financial_adviser.clients.filter(
                    id=pk).get().financialplanning.goal_manager.pk
                fp_and_gm_pks = (
                    {'fp': financial_planning_pk, 'gm': goal_manager_pk})
            except BaseException:
                fp_and_gm_pks = ({'fp': '', 'gm': ''})
        return Response(fp_and_gm_pks)
