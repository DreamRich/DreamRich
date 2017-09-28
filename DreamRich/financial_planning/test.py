from django.test import TestCase
from decimal import Decimal
from financial_planning.factories import RegularCostFactory


class RegularCostTest(TestCase):

    def setUp(self):
        self.regular_cost = RegularCostFactory()

    def test_regulat_cost_total(self):
        total = Decimal('219.60')
        self.assertEqual(self.regular_cost.total, total)
