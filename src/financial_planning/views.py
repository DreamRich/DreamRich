from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from financial_planning.serializers import (
    RegularCostSerializer,
    CostManagerSerializer,
    CostTypeSerializer,
    FinancialPlanningSerializer,
    FlowUnitChangeSerializer,
    FinancialIndependenceSerializer,
    FinancialPlanningFlowSerializer,
)
from financial_planning.models import (
    RegularCost, CostManager,
    CostType, FinancialPlanning,
    FlowUnitChange, FinancialIndependence,
)
from employee.models import FinancialAdviser
from dr_auth.models_permissions import GeneralModelPermissions
from dr_auth.custom_permissions import GeneralCustomPermissions


class CostTypeViewList(generics.ListAPIView):

    serializer_class = CostTypeSerializer
    queryset = CostType.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class RegularCostViewSet(viewsets.ModelViewSet):

    serializer_class = RegularCostSerializer
    queryset = RegularCost.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class CostManagerViewSet(viewsets.ModelViewSet):

    serializer_class = CostManagerSerializer
    queryset = CostManager.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class FinancialPlanningViewSet(viewsets.ModelViewSet):

    serializer_class = FinancialPlanningSerializer
    queryset = FinancialPlanning.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)

    # pylint: disable=invalid-name, unused-argument, no-self-use
    @detail_route(methods=['get'])
    def total_resource_for_annual_goals(self, request, pk=None):
        return Response(FinancialPlanning.objects.filter(pk=pk).get()
                        .total_resource_for_annual_goals)

    @detail_route(methods=['get'])
    def patrimony_flow(self, request, pk=None):
        financial_planning = self.queryset.filter(pk=pk).get()
        data = FinancialPlanningFlowSerializer(financial_planning).data

        return Response(data)

    @detail_route(methods=['get'])
    def respective_clients(self, request, pk=None):
        """
        Return the pk from financial planning and pk goal manager.\
        """
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


class FlowUnitChangeViewSet(viewsets.ModelViewSet):

    serializer_class = FlowUnitChangeSerializer
    queryset = FlowUnitChange.objects.all()
    filter_fields = ('cost_manager_id', 'incomes_id')
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)


class FinancialIndependenceViewSet(viewsets.ModelViewSet):

    serializer_class = FinancialIndependenceSerializer
    queryset = FinancialIndependence.objects.all()
    permission_classes = (GeneralModelPermissions,
                          GeneralCustomPermissions)
