from django.test import TestCase
from decimal import Decimal
from financial_planning.factories import FinancialPlanningFactory
from client.factories import ActiveClientMainFactory
import datetime


class PatrimonyTest(TestCase):

    def setUp(self):
        active_client = ActiveClientMainFactory(birthday=\
                                                datetime.datetime(1977,1,1))
        self.financial_planning = FinancialPlanningFactory(active_client=\
                                                           active_client)

    def test_current_net_investment(self):
        self.assertEqual(
            self.financial_planning.goal_manager.duration_goals, 20)
