import datetime
from django.test import TestCase
from financial_planning.factories import FinancialPlanningFactory
from client.factories import ActiveClientMainFactory
from goal.factories import GoalFactory, GoalTypeFactory


class GoalTest(TestCase):

    def setUp(self):
        active_client = ActiveClientMainFactory(
            birthday=datetime.datetime(1977, 1, 1))
        financial_planning = FinancialPlanningFactory(
            active_client=active_client)
        self.goal_manager = financial_planning.goal_manager
        goal_type1 = GoalTypeFactory(name='Imóvel')
        goal_type2 = GoalTypeFactory(name='Vestuário')
        self.goal_has_end_date = GoalFactory(has_end_date=False,
                                             goal_type=goal_type1,
                                             year_init=2021,
                                             periodicity=3,
                                             value=50000,
                                             goal_manager=self.goal_manager)
        self.goal_hasnt_end_date = GoalFactory(has_end_date=True,
                                               goal_type=goal_type2,
                                               year_init=2021,
                                               periodicity=3,
                                               value=50000,
                                               year_end=2031,
                                               goal_manager=self.goal_manager)
        self.array_flow_withot_date = [0, 0, 0, 0, 50000, 0, 0, 50000, 0, 0,
                                       50000, 0, 0, 50000, 0, 0, 50000, 0, 0,
                                       50000]
        self.array_flow_with_date = [0, 0, 0, 0, 50000, 0, 0, 50000, 0, 0,
                                     50000, 0, 0,
                                     50000, 0, 0, 0, 0, 0, 0]

    def test_flow_hasnt_end_date(self):
        self.assertEqual(self.array_flow_withot_date,
                         self.goal_has_end_date.flow)

    def test_flow_has_end_date(self):
        self.assertEqual(self.array_flow_with_date,
                         self.goal_hasnt_end_date.flow)

    def test_goals_flow_dic(self):
        goals_flow_dic = []
        goal_flow_dic1 = {}
        goal_flow_dic1['name'] = 'Imóvel'
        goal_flow_dic1['data'] = self.array_flow_withot_date
        goal_flow_dic2 = {}
        goal_flow_dic2['name'] = 'Vestuário'
        goal_flow_dic2['data'] = self.array_flow_with_date
        goals_flow_dic.append(goal_flow_dic1)
        goals_flow_dic.append(goal_flow_dic2)

        self.assertEqual(goals_flow_dic, self.goal_manager.goals_flow_dic)

    def test_year_init_to_year_end(self):
        array = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026,
                 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036]
        self.assertEqual(self.goal_manager.year_init_to_year_end, array)

    def test_value_total_by_year(self):
        array = [0, 0, 0, 0, 100000, 0, 0, 100000, 0, 0, 100000, 0, 0, 100000,
                 0, 0, 50000, 0, 0, 50000]
        self.assertEqual(self.goal_manager.value_total_by_year(), array)
