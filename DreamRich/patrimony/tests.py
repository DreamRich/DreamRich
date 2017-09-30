from django.test import TestCase
from decimal import Decimal
from patrimony.factories import PatrimonyMainFactory, IncomeFactory


class PatrimonyTest(TestCase):

    def setUp(self):
        self.patrimony = PatrimonyMainFactory()
        self.common_income = IncomeFactory(value_monthly =\
                                             round(Decimal(1200),2),
                                          thirteenth = False,
                                          patrimony = self.patrimony,
                                          vacation = False)
        self.income_with_thirteenth = IncomeFactory(value_monthly =\
                                                     round(Decimal(1200),2),
                                                   thirteenth = True,
                                                   patrimony = self.patrimony,
                                                   vacation = False)
        self.income_with_vacation = IncomeFactory(value_monthly =\
                                                     round(Decimal(1200),2),
                                                   thirteenth = False,
                                                   patrimony = self.patrimony,
                                                   vacation = True)

    def test_current_net_investment(self):
        self.assertEqual(
            Decimal('0.90'),
            self.patrimony.current_net_investment)

    def test_current_property_investment(self):
        self.assertEqual(Decimal('121.21'),
                         self.patrimony.current_property_investment)

    def test_current_income_generation(self):
        self.assertEqual(Decimal('1345.61'),
                         self.patrimony.possible_income_generation)

    def test_annual_income(self):
        self.assertEqual(self.common_income.annual_income,Decimal(14400.00))

    def test_annual_income_with_thirteen(self):
        self.assertEqual(self.income_with_thirteenth.annual_income,
                         Decimal(15600.00))

    def test_annual_income_with_vacation(self):
        self.assertEqual(self.income_with_vacation.annual_income,
                         Decimal(14800.00))
