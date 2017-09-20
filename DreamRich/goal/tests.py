from django.test import TestCase
from decimal import Decimal
from financial_planning.factories import FinancialPlanningFactory
from client.factories import ActiveClientMainFactory
from goal.factories import GoalFactory, GoalManagerFactory
import datetime


class GoalTest(TestCase):

    def setUp(self):
        active_client = ActiveClientMainFactory(birthday=\
                                                datetime.datetime(1977,1,1))
        financial_planning = FinancialPlanningFactory(active_client=\
                                                           active_client)
        self.goal_manager = financial_planning.goal_manager
        self.goal_periodic = GoalFactory(is_periodic = True,
                                         year_init = 2021,
                                         periodicity = 3,
                                         value = 50000,
                                         goal_manager = self.goal_manager)

    def test_duration_goals(self):
        self.assertEqual(
            self.goal_manager.duration_goals, 20)

    def test_flow_periodicity(self):
        array_flow = [0,0,0,0,50000,0,0,50000,0,0,50000,0,0,50000,0,0,50000,
                      0,0,50000]
        self.assertEqual(array_flow, self.goal_periodic.flow)
