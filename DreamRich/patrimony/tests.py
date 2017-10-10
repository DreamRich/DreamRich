from django.test import TestCase
from patrimony.factories import PatrimonyMainFactory, IncomeFactory
from client.factories import ActiveClientMainFactory
from financial_planning.factories import FinancialPlanningFactory
import datetime


class PatrimonyTest(TestCase):

    def setUp(self):
        active_client = ActiveClientMainFactory(
            birthday=datetime.datetime(1967, 1, 1))
        self.patrimony = PatrimonyMainFactory()
        self.patrimony.income_set.all().update(value_monthly=1212.2)
        financial_planning = FinancialPlanningFactory(  # NOQA
            active_client=active_client,
            patrimony=self.patrimony)
        self.common_income = IncomeFactory(value_monthly=round(1200, 2),
                                           thirteenth=False,
                                           patrimony=self.patrimony,
                                           vacation=False)
        self.income_with_thirteenth = IncomeFactory(value_monthly=1200.00,
                                                    thirteenth=True,
                                                    patrimony=self.patrimony,
                                                    vacation=False)
        self.income_with_vacation = IncomeFactory(value_monthly=round(1200, 2),
                                                  thirteenth=False,
                                                  patrimony=self.patrimony,
                                                  vacation=True)

    def test_current_net_investment(self):
        self.assertEqual(321200.00, self.patrimony.current_net_investment())

    def test_current_property_investment(self):
        self.assertEqual(121.21, self.patrimony.current_property_investment())

    def test_current_income_generation(self):
        self.assertEqual(1345.6100000000001,
                         self.patrimony.possible_income_generation())

    def test_annual_income(self):
        self.assertEqual(self.common_income.annual(), 14400.00)

    def test_annual_income_with_thirteen(self):
        self.assertEqual(self.income_with_thirteenth.annual(), 15600.00)

    def test_annual_income_with_vacation(self):
        self.assertEqual(self.income_with_vacation.annual(), 14800.00)

    def test_current_monthly_income(self):
        self.assertEqual(60962.67, self.patrimony.total_annual_income())

    def test_income_flow(self):
        change_total_annual_income = [0, 0, 0, 0, 500.00, -500.00, 0, 0, 0, 0]
        flow_regular_cost_with_change = [60962.67, 60962.67, 60962.67,
                                         60962.67, 61462.67, 60962.67,
                                         60962.67, 60962.67, 60962.67,
                                         60962.67]

        self.assertEqual(flow_regular_cost_with_change,
                         self.patrimony.
                         income_flow(change_total_annual_income))
