from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from financial_planning.serializers import (
    RegularCostSerializer,
    CostManagerSerializer,
    CostTypeSerializer,
    FinancialPlanningSerializer,
    FlowUnitChangeSerializer,
    FinancialIndependenceSerializer,
)
from financial_planning.models import (
    RegularCost, CostManager,
    CostType, FinancialPlanning,
    FlowUnitChange, FinancialIndependence,
)
from employee.models import FinancialAdviser
from dr_auth.permissions import FinancialPlanningPermission


class CostTypeViewList(generics.ListAPIView):
    """
    retrieve:
        Return a cost type instance.

    list:
        Return all cost types, ordered by most recently joined.

    create:
        Create a new cost type.

    delete:
        Remove an existing cost type.

    partial_update:
        Update one or more fields on an existing cost type.

    update:
        Update a cost type.
    """

    serializer_class = CostTypeSerializer
    queryset = CostType.objects.all()


class RegularCostViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a regular cost instance.

    list:
        Return all regular costs, ordered by most recently joined.

    create:
        Create a new regular cost.

    delete:
        Remove an existing regular cost.

    partial_update:
        Update one or more fields on an existing regular cost.

    update:
        Update a regular cost.
    """

    serializer_class = RegularCostSerializer
    queryset = RegularCost.objects.all()


class CostManagerViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a cost manager instance.

    list:
        Return all cost managers, ordered by most recently joined.

    create:
        Create a new cost manager.

    delete:
        Remove an existing cost manager.

    partial_update:
        Update one or more fields on an existing cost manager.

    update:
        Update a cost manager.
    """

    serializer_class = CostManagerSerializer
    queryset = CostManager.objects.all()


class FinancialPlanningViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a financial planning instance.

    list:
        Return all financial plannings, ordered by most recently joined.

    create:
        Create a new regular financial planning.

    delete:
        Remove an existing regular financial planning.

    partial_update:
        Update one or more fields on an existing financial planning.

    update:
        Update a financial planning.
    """

    serializer_class = FinancialPlanningSerializer
    queryset = FinancialPlanning.objects.all()

    # pylint: disable=invalid-name, unused-argument, no-self-use
    @detail_route(methods=['get'])
    def total_resource_for_annual_goals(self, request, pk=None):
        """
        Return a total resource for annual goal.
        """
        return Response(FinancialPlanning.objects.filter(pk=pk).get()
                        .total_resource_for_annual_goals)

    @detail_route(methods=['get'])
    def respective_clients(self, request, pk=None):
        """
        Return the pk from financial planning and pk goal manager.\
        Permissions: see_own_client_data and see_financial_adviser_data
        """
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


class FlowUnitChangeViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a change in cost or income.

    list:
        Return all changes, ordered by most recently joined.

    create:
        Create a new change in cost or income.

    delete:
        Remove an existing change in cost or income.

    partial_update:
        Update one or more fields on an existing change.

    update:
        Update a change in flow.
    """
    serializer_class = FlowUnitChangeSerializer
    queryset = FlowUnitChange.objects.all()
    filter_fields = ('cost_manager_id', 'incomes_id')


class FinancialIndependenceViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a financial independence instance.

    list:
        Return all financial independences, ordered by most recently joined.

    create:
        Create a new financial independence.

    delete:
        Remove an existing financial independence.

    partial_update:
        Update one or more fields on an existing financial independence.

    update:
        Update a financial independence.
    """

    serializer_class = FinancialIndependenceSerializer
    queryset = FinancialIndependence.objects.all()
