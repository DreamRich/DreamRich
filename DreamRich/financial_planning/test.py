from django.test import TestCase
from decimal import Decimal
from client.factories import ActiveClientMainFactory
from financial_planning.factories import (
        RegularCostFactory,
        FinancialPlanningFactory
)
import datetime

class FinancialPlanningTest(TestCase):
    def setUp(self):
        self.regular_cost = RegularCostFactory()
        active_client = ActiveClientMainFactory(
        birthday=datetime.datetime(1967, 1, 1))
        self.financial_planning = FinancialPlanningFactory(
                                     active_client=active_client,
                                     regular_cost=self.regular_cost,
                                     )
        self.non_change_regular_cost = [0, 0, 0, 0, Decimal('123.40'),
                                        Decimal('-123.40'), 0, 0, 0, 0]
        self.flow_regular_cost_without_change = [Decimal('219.60'),
                                                 Decimal('219.60'),
                                                 Decimal('219.60'),
                                                 Decimal('219.60'),
                                                 Decimal('343.00'),
                                                 Decimal('219.60'),
                                                 Decimal('219.60'),
                                                 Decimal('219.60'),
                                                 Decimal('219.60'),
                                                 Decimal('219.60'),
                                                ]

    def test_duration_financial_planning(self):
        self.assertEqual(
             self.financial_planning.duration(), 10)

    def test_regulat_cost_total(self):
        total = Decimal('219.60')
        self.assertEqual(self.regular_cost.total(), total)

    def test_regular_cost_flow_withot_change(self):
        self.assertEqual(self.flow_regular_cost_without_change,
                         self.regular_cost.flow(self.non_change_regular_cost))
