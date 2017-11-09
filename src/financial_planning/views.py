from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
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
from dr_auth.permissions import FinancialPlanningPermission


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

    # pylint: disable=invalid-name, unused-argument, no-self-use
    @detail_route(methods=['get'])
    def total_resource_for_annual_goals(self, request, pk=None):
        return Response(FinancialPlanning.objects.filter(pk=pk).get()
                        .total_resource_for_annual_goals)

    @detail_route(methods=['get'])
    def respective_clients(self, request, pk=None):
        if FinancialPlanningPermission.has_permission_to_see_chart(
                request.user):
            current_financial_adviser = FinancialAdviser.objects.filter(
                id=self.request.user.id).get()

            # fp = Financial Planning and gm = Goal Manager
            fp_and_gm_pks = ()

            if current_financial_adviser.clients.filter(pk=pk).exists():
                try:
                    goal_manager_pk = current_financial_adviser.clients.filter(
                        id=pk).get().financialplanning.goal_manager.pk
                    fp_and_gm_pks = (
                        {'fp': pk, 'gm': goal_manager_pk})
                except BaseException:
                    fp_and_gm_pks = ({'fp': '', 'gm': ''})
            return Response(fp_and_gm_pks)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
