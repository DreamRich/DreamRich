from django.test import TestCase
from client.factories import ActiveClientMainFactory
from goal.factories import (
    GoalManagerFactory,
    GoalFactory,
)
from patrimony.factories import (
    PatrimonyMainFactory,
    ActiveFactory,
    ArrearageFactory,
)
from financial_planning.factories import (
    RegularCostFactory,
    FinancialIndependenceFactory,
    FinancialPlanningFactory
)
import datetime


class FinancialPlanningTest(TestCase):
    def setUp(self):
        self.regular_cost = RegularCostFactory()
        active_client = ActiveClientMainFactory(
            birthday = datetime.datetime(1967, 1, 1))
        self.patrimony = PatrimonyMainFactory()
        self.patrimony.income_set.all().update(value_monthly = 55000,
                                               thirteenth = False,
                                               vacation = False)
        active = ActiveFactory(patrimony = self.patrimony, value = 30000.00)  # NOQA
        active_2 = ActiveFactory(patrimony = self.patrimony,
                                             value = 321200.00)  # NOQA
        arrerage = ArrearageFactory(patrimony = self.patrimony,
                                                value = 351200.00)  # NOQA
        goal_manager = GoalManagerFactory()
        GoalFactory.create_batch(4,
                                 goal_manager = goal_manager,
                                 year_init = 2017,
                                 year_end = 2027,
                                 value = 2500,
                                 periodicity = 1)
        self.financial_independece = FinancialIndependenceFactory(
            duration_of_usufruct = 35,
            remain_patrimony = 30000,
        )
        self.financial_planning = FinancialPlanningFactory(
            active_client = active_client,
            regular_cost = self.regular_cost,
            patrimony = self.patrimony,
            financial_independence = self.financial_independece,
            goal_manager = goal_manager,
        )

    def test_duration_financial_planning(self):
        self.assertEqual(
            self.financial_planning.duration(), 10)

    def test_regular_cost_total(self):
        total = 219.5999999999994
        self.assertAlmostEqual(self.regular_cost.total(), total, 4)

    def test_regular_cost_flow_withot_change(self):
        change_regular_cost = [0, 0, 0, 0, 123.40, -123.40, 0, 0, 0, 0]
        flow_regular_cost_change = [219.59999999999994, 219.59999999999994,
                                    219.59999999999994, 219.59999999999994,
                                    342.99999999999994, 219.59999999999994,
                                    219.59999999999994, 219.59999999999994,
                                    219.59999999999994, 219.59999999999994]
        self.assertEqual(flow_regular_cost_change,
                         self.regular_cost.flow(change_regular_cost))

    def test_assets_required(self):
        self.assertAlmostEqual(self.financial_independece.assets_required(),
                               6447963.5463578859,
                               4)

    def test_remain_necessary_for_retirement(self):
        self.financial_planning.active_client.\
            birthday = datetime.datetime(1978, 1, 1)
        self.assertAlmostEqual(self.financial_independece.
                               remain_necessary_for_retirement(),
                               12156.118288258309, 4)

    def test_real_gain_related_cdi(self):
        data = {}
        data[80] = (0.02050232558139542)
        data[85] = (0.026144186046511697)
        data[90] = (0.031786046511627974)
        data[95] = (0.03742790697674425)
        data[100] = (0.04306976744186053)
        data[105] = (0.04871162790697681)
        data[110] = (0.054353488372093084)
        data[115] = (0.05999534883720936)
        data[120] = (0.06563720930232564)
        data[125] = (0.07127906976744192)
        data[130] = (0.0769209302325582)
        data[135] = (0.08256279069767447)
        data[140] = (0.08820465116279075)
        data[145] = (0.09384651162790703)
        data[150] = (0.0994883720930233)
        data[155] = (0.10513023255813958)
        data[160] = (0.11077209302325586)
        data[165] = (0.11641395348837213)
        data[170] = (0.12205581395348841)
        data[175] = (0.1276976744186047)
        data[180] = (0.13333953488372097)
        data[185] = (0.13898139534883724)
        data[190] = (0.14462325581395352)
        data[195] = (0.1502651162790698)
        data[200] = (0.15590697674418608)
        self.assertAlmostEqual(self.financial_planning.
                               real_gain_related_cdi(), data)

    def test_create_array_change_annual(self):
        change = {2018: 2000, 2020: -5000}
        array_compare = [0, 2000, 0, -5000, 0, 0, 0, 0, 0, 0]
        self.assertEqual(self.financial_planning.create_array_change_annual(
                                                 change), array_compare)

    def test_annual_leftovers_for_goal_without_change(self):
        array = [609470.63389720698, 609470.63389720698,  609470.63389720698,
                 609470.63389720698, 609470.63389720698,  609470.63389720698,
                 609470.63389720698, 609470.63389720698,  609470.63389720698,
                 609470.63389720698]
        self.assertEqual(self.financial_planning.annual_leftovers_for_goal(),
                         array)
    def test_annual_leftovers_for_goal_with_change(self):
        change_income = {2018: 2000}
        change_cost = {2017: 2000, 2026: 9000}
        array = [607470.63389720698, 609470.63389720698,  609470.63389720698,
                 609470.63389720698, 609470.63389720698,  609470.63389720698,
                 609470.63389720698, 609470.63389720698,  609470.63389720698,
                 600470.63389720698]
        self.assertEqual(self.financial_planning.annual_leftovers_for_goal(
                                        change_income, change_cost), array)
