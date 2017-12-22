import datetime
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from client.factories import ActiveClientFactory
from goal.factories import (
    GoalManagerFactory, GoalFactory,
    GoalTypeFactory,
)
from patrimony.factories import (
    PatrimonyFactory, ActiveFactory,
    ArrearageFactory,
)
from lib.financial_planning.flow import create_array_change_annual
from lib.tests import test_all_create_historic
from protection.factories import (
    ProtectionManagerFactory, LifeInsuranceFactory
)
from financial_planning.factories import (
    CostManagerFactory, FinancialIndependenceFactory,
    FinancialPlanningFactory,
)
from financial_planning.models import (
    RegularCost, FinancialIndependence,
    FinancialPlanning, FlowUnitChange
)


class FinancialIndependencePlanningTest(TestCase):
    def setUp(self):
        self.financial_independence = FinancialIndependenceFactory(
            duration_of_usufruct=35,
            remain_patrimony=30000,
        )
        active_client = ActiveClientFactory(
            birthday=datetime.datetime(1967, 1, 1))
        self.financial_planning = FinancialPlanningFactory(
            active_client=active_client,
            financial_independence=self.financial_independence,
        )

    def test_assets_required(self):
        self.assertAlmostEqual(self.financial_independence.assets_required(),
                               6447963.5463578859,
                               4)

    def test_remain_necessary_for_retirement_with_high_patrimony(self):
        active_manager = self.financial_planning.patrimony.activemanager
        active_manager.actives.update(value=30021200.00)
        self.assertEqual(self.financial_independence.
                         remain_necessary_for_retirement(), 0)

    def test_remain_necessary_for_retirement(self):
        self.financial_planning.active_client.\
            birthday = datetime.datetime(1978, 1, 1)
        self.assertAlmostEqual(self.financial_independence.
                               remain_necessary_for_retirement(),
                               12156.118288258309, 4)


class FinancialIndependencePatrimonyTest(TestCase):
    def setUp(self):
        active_client = ActiveClientFactory(
            birthday=datetime.datetime(1967, 1, 1))
        financial_planning = FinancialPlanningFactory(
            active_client=active_client)
        goal_manager = financial_planning.goal_manager
        self.financial_independence = financial_planning.financial_independence
        self.financial_independence.rate = 0.02

        goals_type = [{'name': 'Casa Extra'},
                      {'name': 'Compra De Cotas Societárias'},
                      {'name': 'Moradia'},
                      {'name': 'Reforma e Manutenção Da Casa'},
                      {'name': 'Viagens'}]

        data_goal_type = []
        for goal_type in goals_type:
            data_goal_type.append(GoalTypeFactory(**goal_type))

        goals = [{'value': 200000, 'init_year': 2018, 'end_year': 2018},
                 {'value': 500000, 'init_year': 2022, 'end_year': 2022},
                 {'value': 1000000, 'init_year': 2021, 'end_year': 2021},
                 {'value': 140000, 'init_year': 2025, 'end_year': 2025},
                 {'value': 50000, 'init_year': 2023, 'end_year': 2023}]

        self.data_goals = []
        for goal_type, goal in zip(data_goal_type, goals):
            self.data_goals.append(GoalFactory(**goal, goal_type=goal_type,
                                               goal_manager=goal_manager))

    def test_filter_goals_that_will_be_monetized(self):
        data = self.financial_independence.\
            filter_goals_that_will_be_monetized()
        sorted(data, key=lambda goal: goal.goal_type.name)
        # Remove 'Viagens', because this goal won't be monetized
        del self.data_goals[-1]
        self.assertEqual(self.data_goals, data)

    def test_goals_monetized(self):
        self.assertAlmostEqual(self.financial_independence.goals_monetized(),
                               2062877.3345884625)

    def test_patrimony_at_end(self):
        self.assertAlmostEqual(self.financial_independence.patrimony_at_end(),
                               6377329.7596444273)


class RegularCostTest(TestCase):
    def setUp(self):
        self.cost_manager = CostManagerFactory()
        active_client = ActiveClientFactory(
            birthday=datetime.datetime(1967, 1, 1))
        self.financial_planning = FinancialPlanningFactory(
            active_client=active_client,
            cost_manager=self.cost_manager,
        )

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


class FinancialPlanningModelTest(TestCase):
    def setUp(self):
        active_client = ActiveClientFactory(
            birthday=datetime.datetime(1967, 1, 1))
        self.financial_planning = FinancialPlanningFactory(
            active_client=active_client,
            target_profitability=1.10,
            cdi=0.1213,
            ipca=0.075
        )

    def test_duration_financial_planning(self):
        self.assertEqual(
            self.financial_planning.duration(), 10)

    def test_real_gain_related_cdi(self):
        self.assertAlmostEqual(self.financial_planning.
                               real_gain_related_cdi(), 0.054353488372093084)

    def test_real_gain(self):
        self.assertAlmostEqual(self.financial_planning.real_gain(),
                               0.04306976744186053)

    def test_save_financial_planning(self):
        financial_planning = FinancialPlanningFactory(init_year=None)
        self.assertEqual(financial_planning.init_year,
                         datetime.datetime.now().year)

    def test_end_year(self):
        self.assertEqual(self.financial_planning.end_year(), 2027)


class FinancialPlanningFlowTest(TestCase):
    def setUp(self):
        self.cost_manager = CostManagerFactory()
        active_client = ActiveClientFactory(
            birthday=datetime.datetime(1967, 1, 1))
        self.patrimony = PatrimonyFactory()
        self.patrimony.incomes.all().update(value_monthly=55000,
                                            thirteenth=False,
                                            vacation=False)

        for active in self.patrimony.activemanager.actives.all():
            active.delete()

        data = [{'value': 30000.00, 'rate': 1.1879},
                {'value': 321200.00, 'rate': 0.7500},
                {'value': 351200.00, 'rate': 0.7500}]

        for active in data:
            ActiveFactory(**active,
                          active_manager=self.patrimony.activemanager)

        ArrearageFactory(patrimony=self.patrimony, value=351200.00)
        self.goal_manager = GoalManagerFactory()
        GoalFactory.create_batch(4,
                                 goal_manager=self.goal_manager,
                                 init_year=2017,
                                 end_year=2027,
                                 value=2500,
                                 periodicity=1)
        self.financial_independence = FinancialIndependenceFactory(
            duration_of_usufruct=35,
            remain_patrimony=30000,
        )
        self.financial_planning = FinancialPlanningFactory(
            active_client=active_client,
            cost_manager=self.cost_manager,
            patrimony=self.patrimony,
            financial_independence=self.financial_independence,
            goal_manager=self.goal_manager,
            cdi=0.1213,
        )
        protection_manager = ProtectionManagerFactory(
            financial_planning=self.financial_planning)

        for private_pension in protection_manager.private_pensions.all():
            private_pension.delete()

        for life_insurance in protection_manager.life_insurances.all():
            life_insurance.delete()

        LifeInsuranceFactory(protection_manager=protection_manager,
                             value_to_pay_annual=2000, has_year_end=False)

    def test_annual_leftovers_for_goal_without_change(self):
        array = [607045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257, 607045.13144555257, 607045.13144555257,
                 607045.13144555257]
        self.assertEqual(self.financial_planning.annual_leftovers_for_goal(),
                         array)

    def test_annual_leftovers_without_change(self):
        array = [647364.8, 647364.8, 647364.8, 647364.8, 647364.8, 647364.8,
                 647364.8, 647364.8, 647364.8, 647364.8]
        self.assertEqual(self.financial_planning.annual_leftovers(), array)

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
                                 init_year=2017,
                                 end_year=2027,
                                 value=65865,
                                 periodicity=1)
        array = [341585.13144555251, 413413.10143097816, 491145.17214779771,
                 573102.25206646265, 659513.98517549736, 750622.49741528649,
                 846683.07511569967, 947964.88030916872, 1054751.7049235257,
                 1167342.7659678517]

        self.assertEqual(self.financial_planning.
                         total_resource_for_annual_goals, array)

    def test_suggested_flow_patrimony(self):
        array = [647364.8, 1319372.6002455815, 2027906.368647767,
                 2774951.418992036, 3562600.973793622, 4393062.0295134,
                 5268661.54056872, 6191852.939466794, 7165223.011330091,
                 8191499.142076154]

        self.assertEqual(self.financial_planning
                         .suggested_flow_patrimony['flow'], array)

    def test_actual_flow_patrimony(self):
        array = [647364.8, 1295546.2297445768, 1954727.8567590017,
                 2625096.3638675935, 3306841.6020630263, 4000156.644272876,
                 4705237.840038632, 5422284.871122657, 6151500.808058847,
                 6893092.167663001]

        self.assertEqual(self.financial_planning.actual_flow_patrimony['flow'],
                         array)


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


class FlowUnitChangeTest(TestCase):

    def setUp(self):
        self.cost_manager = CostManagerFactory()
        self.incomes = PatrimonyFactory()

    def test_validation_cost_manager_and_incomes_null_together(self):
        change = FlowUnitChange(annual_value=123.40, year=2021)
        with self.assertRaises(ValidationError):
            change.save()

    def test_validation_cost_manager_and_incomes_instanciate(self):
        change = FlowUnitChange(
            annual_value=123.40,
            year=2021,
            cost_manager=self.cost_manager,
            incomes=self.incomes)
        with self.assertRaises(ValidationError):
            change.save()

    def test_validation_cost_manager_instaciate_only(self):
        change = FlowUnitChange.objects.create(annual_value=123.40, year=2021,
                                               cost_manager=self.cost_manager)
        self.assertTrue(change.cost_manager is not None)

    def test_validation_incomes_instaciate_only(self):
        change = FlowUnitChange.objects.create(annual_value=123.40, year=2021,
                                               incomes=self.incomes)
        self.assertTrue(change.incomes is not None)


class HistoricalFinancialPlanningCreateTest(TestCase):

    def flow_change_case(self, model):
        self.assertEqual(model.history.count(), 0)
        model.objects.create(year=2020, annual_value=1233,
                             cost_manager=CostManagerFactory())
        self.assertTrue(model.history.count() > 0)

    def test_flow_change(self):
        self.flow_change_case(FlowUnitChange)

    def test_all_models(self):
        models = [FinancialIndependence, FinancialPlanning, RegularCost]
        test_all_create_historic(self, models, FinancialPlanningFactory)
