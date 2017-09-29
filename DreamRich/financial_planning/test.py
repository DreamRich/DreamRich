from django.test import TestCase
from decimal import Decimal
from client.factories import ActiveClientMainFactory
from financial_planning.factories import (
        RegularCostFactory,
        FinancialPlanningFactory
)
import datetime


class RegularCostTest(TestCase):

    def setUp(self):
        self.regular_cost = RegularCostFactory()

    def test_regulat_cost_total(self):
        total = Decimal('219.60')
        self.assertEqual(self.regular_cost.total(), total)

class FinancialPlanningTest(TestCase):
     def setUp(self):
         active_client = ActiveClientMainFactory(
         birthday=datetime.datetime(1977, 1, 1))
         self.financial_planning = FinancialPlanningFactory(
                                     active_client=active_client)

     def test_duration_financial_planning(self):
         self.assertEqual(
                 self.financial_planning.duration_financial_planning(), 20)
