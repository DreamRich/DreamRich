from django.test import TestCase
from decimal import Decimal
from patrimony.factories import PatrimonyMainFactory, IncomeFactory
from client.factories import ActiveClientMainFactory
from financial_planning.factories import FinancialPlanningFactory
import datetime


class PatrimonyTest(TestCase):

    def setUp(self):
        active_client = ActiveClientMainFactory(
                            birthday=datetime.datetime(1967, 1, 1))
        self.patrimony = PatrimonyMainFactory()
        financial_planning = FinancialPlanningFactory(
                                active_client=active_client,
                                patrimony=self.patrimony)
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
            Decimal('321200.00'),
            self.patrimony.current_net_investment())

    def test_current_property_investment(self):
        self.assertEqual(Decimal('121.21'),
                         self.patrimony.current_property_investment())

    def test_current_income_generation(self):
        self.assertEqual(Decimal('1345.61'),
                         self.patrimony.possible_income_generation())

    def test_annual_income(self):
        self.assertEqual(self.common_income.annual(),Decimal(14400.00))

    def test_annual_income_with_thirteen(self):
        self.assertEqual(self.income_with_thirteenth.annual(),
                         Decimal(15600.00))

    def test_annual_income_with_vacation(self):
        self.assertEqual(self.income_with_vacation.annual(),
                         Decimal(14800.00))

    def test_current_monthly_income(self):
        self.assertEqual(Decimal('60962.67'),
                         self.patrimony.total_annual_income())

    def test_income_flow(self):
        change_total_annual_income = [0, 0, 0, 0, Decimal('500.00'),
                                            Decimal('-500.00'), 0, 0, 0, 0]
        flow_regular_cost_with_change = [Decimal('60962.67'),
                                         Decimal('60962.67'),
                                         Decimal('60962.67'),
                                         Decimal('60962.67'),
                                         Decimal('61462.67'),
                                         Decimal('60962.67'),
                                         Decimal('60962.67'),
                                         Decimal('60962.67'),
                                         Decimal('60962.67'),
                                         Decimal('60962.67'),
                                         ]

        self.assertEqual(flow_regular_cost_with_change,
                     self.patrimony.income_flow(change_total_annual_income))
