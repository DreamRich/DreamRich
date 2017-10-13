from django.test import TestCase, Client
from client.factories import ActiveClientMainFactory
from patrimony.factories import (
    PatrimonyMainFactory,
    ActiveFactory,
    ArrearageFactory,
)
from financial_planning.factories import (
    CostManagerFactory,
    FinancialIndependenceFactory,
    FinancialPlanningFactory
)
import datetime


class FinancialPlanningTest(TestCase):
    def setUp(self):
        self.cost_manager = CostManagerFactory()
        active_client = ActiveClientMainFactory(
            birthday=datetime.datetime(1967, 1, 1))
        self.patrimony = PatrimonyMainFactory()
        active = ActiveFactory(patrimony=self.patrimony, value=30000.00)  # NOQA
        active_2 = ActiveFactory(patrimony=self.patrimony, value=321200.00)  # NOQA
        arrerage = ArrearageFactory(patrimony=self.patrimony, value=351200.00)  # NOQA
        self.financial_independece = FinancialIndependenceFactory(
            duration_of_usufruct=35,
            remain_patrimony=30000,
        )
        self.financial_planning = FinancialPlanningFactory(
            active_client=active_client,
            cost_manager=self.cost_manager,
            patrimony=self.patrimony,
            financial_independence=self.financial_independece
        )

    def test_duration_financial_planning(self):
        self.assertEqual(
            self.financial_planning.duration(), 10)

    def test_cost_manager_total(self):
        total = 219.5999999999994
        self.assertAlmostEqual(self.cost_manager.total(), total, 4)

    def test_regular_cost_flow_withot_change(self):
        change_regular_cost = [0, 0, 0, 0, 123.40, -123.40, 0, 0, 0, 0]
        flow_regular_cost_change = [219.59999999999994, 219.59999999999994,
                                    219.59999999999994, 219.59999999999994,
                                    342.99999999999994, 219.59999999999994,
                                    219.59999999999994, 219.59999999999994,
                                    219.59999999999994, 219.59999999999994]
        self.assertEqual(flow_regular_cost_change,
                         self.cost_manager.flow(change_regular_cost))

    def test_assets_required(self):
        self.assertAlmostEqual(self.financial_independece.assets_required(),
                               6447963.5463578859,
                               4)

    def test_remain_necessary_for_retirement(self):
        self.financial_planning.active_client.\
            birthday = datetime.datetime(1978, 1, 1)
        self.assertAlmostEqual(self.financial_independece.
                               remain_necessary_for_retirement(),
                               12147.728680592305, 4)


class RegularCostViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.manager = CostManagerFactory()

    def test_get_view(self):
        pk = self.manager.pk
        response = self.client.get('/api/financial_planning/costmanager/'
                                   '{}/'.format(pk))
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        response = self.client.post('/api/financial_planning/costmanager', {},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [('/api/financial_planning/costmanager/', 301)])

    def test_delete_view(self):
        pk = self.manager.pk
        response = self.client.delete('/api/financial_planning/costmanager/'
                                      '{}/'.format(pk))
        self.assertEqual(response.status_code, 204)

    def test_update_view(self):
        pk = self.manager.pk
        response = self.client.put('/api/financial_planning/costmanager/'
                                   '{}/'.format(pk))
        self.assertEqual(response.status_code, 200)
