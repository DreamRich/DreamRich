from django.test import TestCase
from financial_planning.factories import (
    FinancialPlanningFactory,
    RegularCostFactory
)
from patrimony.factories import ActiveFactory


class EmergencyReserveTest(TestCase):

    def setUp(self):
        financial_planning = FinancialPlanningFactory()
        self.active_manager = financial_planning.patrimony.activemanager
        patrimony = financial_planning.patrimony
        self.emergency_reserve = financial_planning.protection_manager.\
            emergency_reserve
        self.emergency_reserve.mounth_of_protection = 12

        for active in self.active_manager.actives.all():
            active.delete()

        cost_manager = financial_planning.cost_manager

        for regular_cost in cost_manager.regular_costs.all():
            regular_cost.delete()

        for arrearage in patrimony.arrearages.all():
            arrearage.delete()

        regular_costs = [{'value': 500}, {'value': 1500}, {'value': 2500}]

        for regular_cost in regular_costs:
            RegularCostFactory(**regular_cost, cost_manager=cost_manager)

    def test_necessery_value(self):
        self.assertEqual(self.emergency_reserve.necessery_value(), 54000)

    def test_risk_gap_on_limit(self):
        ActiveFactory(value=54000, active_manager=self.active_manager)
        self.assertEqual(self.emergency_reserve.risk_gap(), 0)

    def test_risk_gap_bigger_limit(self):
        ActiveFactory(value=59000, active_manager=self.active_manager)
        self.assertEqual(self.emergency_reserve.risk_gap(), 0)

    def test_risk_gap_less_limit(self):
        ActiveFactory(value=51000, active_manager=self.active_manager)
        self.assertEqual(self.emergency_reserve.risk_gap(), 3000)
