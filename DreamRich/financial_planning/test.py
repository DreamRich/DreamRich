from django.test import TestCase
from client.factories import ActiveClientMainFactory
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
            regular_cost=self.regular_cost,
            patrimony=self.patrimony,
            financial_independence=self.financial_independece
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
                               12147.728680592305, 4)
