from django.test import TestCase
from decimal import Decimal
from patrimony.factories import PatrimonyFactory


class PatrimonyTest(TestCase):
    def setUp(self):
      self.patrimony = PatrimonyFactory()
      self.current_net_investment_test = Decimal('0.90')
      self.current_property_investment_test = Decimal('121.21')
      self.possible_income_generation_test = Decimal('1345.61')
      self.current_monthly_income_test = Decimal('1414.23')

    def test_current_net_investment(self):
        self.assertEqual(self.current_net_investment_test,self.patrimony.current_net_investment)

    def test_current_property_investment(self):
        self.assertEqual(self.current_property_investment_test,self.patrimony.current_property_investment)

    def test_current_net_investment(self):
        self.assertEqual(self.possible_income_generation_test,self.patrimony.possible_income_generation)

    def test_current_net_investment(self):
        self.assertEqual(self.current_monthly_income_test,self.patrimony.current_monthly_income)
