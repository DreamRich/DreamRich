import datetime
from django.test import TestCase, Client
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
from lib.financial_planning.flow import create_array_change_annual
from financial_planning.models import FlowUnitChange
from financial_planning.factories import (
    CostManagerFactory,
    FinancialIndependenceFactory,
    FinancialPlanningFactory
)


class FinancialPlanningTest(TestCase):
    def setUp(self):
        self.cost_manager = CostManagerFactory()
        active_client = ActiveClientMainFactory(
            birthday=datetime.datetime(1967, 1, 1))
        self.patrimony = PatrimonyMainFactory()
        self.patrimony.incomes.all().update(value_monthly=55000,
                                            thirteenth=False,
                                            vacation=False)
        ActiveFactory(value=30000.00,
                      active_manager=self.patrimony.activemanager)
        ActiveFactory(value=321200.00,
                      active_manager=self.patrimony.activemanager)
        ArrearageFactory(patrimony=self.patrimony, value=351200.00)
        self.goal_manager = GoalManagerFactory()
        GoalFactory.create_batch(4,
                                 goal_manager=self.goal_manager,
                                 year_init=2017,
                                 year_end=2027,
                                 value=2500,
                                 periodicity=1)
        self.financial_independece = FinancialIndependenceFactory(
            duration_of_usufruct=35,
            remain_patrimony=30000,
        )
        self.financial_planning = FinancialPlanningFactory(
            active_client=active_client,
            cost_manager=self.cost_manager,
            patrimony=self.patrimony,
            financial_independence=self.financial_independece,
            goal_manager=self.goal_manager,
            target_profitability=110,
        )

    def test_duration_financial_planning(self):
        self.assertEqual(
            self.financial_planning.duration(), 10)

    def test_cost_manager_total(self):
        total = 219.5999999999994
        self.assertAlmostEqual(self.cost_manager.total(), total, 4)

    def test_regular_cost_flow_with_change(self):
        FlowUnitChange.objects.create(annual_value=123.40, year=2021,
                                      cost_manager=self.cost_manager)
        FlowUnitChange.objects.create(annual_value=-123.40, year=2022,
                                      cost_manager=self.cost_manager)

        flow_regular_cost_change = [2635.1999999999994, 2635.1999999999994,
                                    2635.1999999999994, 2635.1999999999994,
                                    2758.5999999999995, 2635.1999999999994,
                                    2635.1999999999994, 2635.1999999999994,
                                    2635.1999999999994, 2635.1999999999994]

        self.assertEqual(flow_regular_cost_change, self.cost_manager.flow())

    def test_assets_required(self):
        self.assertAlmostEqual(self.financial_independece.assets_required(),
                               6447963.5463578859,
                               4)

    def test_remain_necessary_for_retirement_with_high_patrimony(self):
        active_manager = self.patrimony.activemanager
        active_manager.actives.update(value=30021200.00)
        self.assertEqual(self.financial_independece.
                         remain_necessary_for_retirement(), 0)

    def test_remain_necessary_for_retirement(self):
        self.financial_planning.active_client.\
            birthday = datetime.datetime(1978, 1, 1)
        self.assertAlmostEqual(self.financial_independece.
                               remain_necessary_for_retirement(),
                               12156.118288258309, 4)

    def test_real_gain_related_cdi(self):
        data = {80: 0.02050232558139542, 85: 0.026144186046511697,
                90: 0.031786046511627974, 95: 0.03742790697674425,
                100: 0.04306976744186053, 105: 0.04871162790697681,
                110: 0.054353488372093084, 115: 0.05999534883720936,
                120: 0.06563720930232564, 125: 0.07127906976744192,
                130: 0.0769209302325582, 135: 0.08256279069767447,
                140: 0.08820465116279075, 145: 0.09384651162790703,
                150: 0.0994883720930233, 155: 0.10513023255813958,
                160: 0.11077209302325586, 165: 0.11641395348837213,
                170: 0.12205581395348841, 175: 0.1276976744186047,
                180: 0.13333953488372097, 185: 0.13898139534883724,
                190: 0.14462325581395352, 195: 0.1502651162790698,
                200: 0.15590697674418608}
        self.assertAlmostEqual(self.financial_planning.
                               real_gain_related_cdi(), data)

    def test_annual_leftovers_for_goal_without_change(self):
        array = [607045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257]
        self.assertEqual(self.financial_planning.annual_leftovers_for_goal(),
                         array)

    def test_annual_leftovers_for_goal_with_change(self):
        FlowUnitChange.objects.create(annual_value=2000.00, year=2018,
                                      incomes=self.patrimony)
        FlowUnitChange.objects.create(annual_value=2000.00, year=2017,
                                      cost_manager=self.cost_manager)
        FlowUnitChange.objects.create(annual_value=9000.00, year=2026,
                                      cost_manager=self.cost_manager)

        array = [605045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257, 607045.13144555257, 607045.13144555257,
                 598045.13144555257]
        self.assertEqual(self.financial_planning.annual_leftovers_for_goal(),
                         array)

    def test_total_resource_for_annual_goals(self):
        FlowUnitChange.objects.create(annual_value=2000.00, year=2018,
                                      incomes=self.patrimony)
        FlowUnitChange.objects.create(annual_value=2000.00, year=2017,
                                      cost_manager=self.cost_manager)
        FlowUnitChange.objects.create(annual_value=9000.00, year=2026,
                                      cost_manager=self.cost_manager)
        GoalFactory.create_batch(4,
                                 goal_manager=self.goal_manager,
                                 year_init=2017,
                                 year_end=2027,
                                 value=65865,
                                 periodicity=1)
        array = [341585.13144555251, 413413.10143097816, 491145.17214779771,
                 573102.25206646265, 659513.98517549736, 750622.49741528649,
                 846683.07511569967, 947964.88030916872, 1054751.7049235257,
                 1167342.7659678517]

        self.assertEqual(self.financial_planning.
                         total_resource_for_annual_goals, array)

    def test_save_financial_planning(self):
        financial_planning = FinancialPlanningFactory(init_year=None)
        self.assertEqual(financial_planning.init_year,
                         datetime.datetime.now().year)

    def test_end_year(self):
        self.assertEqual(self.financial_planning.end_year(), 2027)


class RegularCostViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.manager = CostManagerFactory()

    def test_get_view(self):
        primary_key = self.manager.pk
        response = self.client.get('/api/financial_planning/cost_manager/'
                                   '{}/'.format(primary_key))
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        response = self.client.post('/api/financial_planning/cost_manager', {},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [('/api/financial_planning/cost_manager/', 301)])

    def test_delete_view(self):
        primary_key = self.manager.pk
        response = self.client.delete('/api/financial_planning/cost_manager/'
                                      '{}/'.format(primary_key))
        self.assertEqual(response.status_code, 204)

    def test_update_view(self):
        primary_key = self.manager.pk
        response = self.client.put('/api/financial_planning/cost_manager/'
                                   '{}/'.format(primary_key))
        self.assertEqual(response.status_code, 200)


class FlowTest(TestCase):
    changes = []
    change1 = FlowUnitChange(year=2018, annual_value=2000)
    changes.append(change1)
    change2 = FlowUnitChange(year=2020, annual_value=-5000)
    changes.append(change2)

    def test_create_array_change_annual(self):
        array_compare = [0, 2000, 0, -5000, 0, 0, 0, 0, 0, 0]
        self.assertEqual(array_compare, create_array_change_annual(
            self.changes, 10, 2017))
