import datetime
from django.test import TestCase
from financial_planning.factories import (
    FinancialPlanningFactory,
    RegularCostFactory
)
from patrimony.factories import ActiveFactory
from protection.factories import (
    PrivatePensionFactory,
    LifeInsuranceFactory,
    EmergencyReserveFactory,
    ReserveInLackFactory,
    ActualPatrimonyProtectionFactory,
    IndependencePatrimonyProtectionFactory,
)
from client.factories import ActiveClientMainFactory


class EmergencyReserveTest(TestCase):

    def setUp(self):
        financial_planning = FinancialPlanningFactory()
        self.active_manager = financial_planning.patrimony.activemanager
        patrimony = financial_planning.patrimony
        self.emergency_reserve = EmergencyReserveFactory(
                                 mounth_of_protection=12,
                                 patrimony=patrimony,
                                 cost_manager=financial_planning.cost_manager)

        for active in self.active_manager.actives.all():
            active.delete()

        cost_manager = financial_planning.cost_manager

        for regular_cost in cost_manager.regular_costs.all():
            regular_cost.delete()

        for arrearage in patrimony.arrearages.all():
            arrearage.delete()

        regular_costs = [{'value': 500}, {'value': 1500}, {'value': 2500}]

        for regular_cost in regular_costs:
            RegularCostFactory(**regular_cost, cost_manager=cost_manager)

    def test_necessery_value(self):
        self.assertEqual(self.emergency_reserve.necessery_value(), 54000)

    def test_risk_gap_on_limit(self):
        ActiveFactory(value=54000, active_manager=self.active_manager)
        self.assertEqual(self.emergency_reserve.risk_gap(), 0)

    def test_risk_gap_bigger_limit(self):
        ActiveFactory(value=59000, active_manager=self.active_manager)
        self.assertEqual(self.emergency_reserve.risk_gap(), 0)

    def test_risk_gap_less_limit(self):
        ActiveFactory(value=51000, active_manager=self.active_manager)
        self.assertEqual(self.emergency_reserve.risk_gap(), 3000)


class ReserveInLackTest(TestCase):
    def setUp(self):
        financial_planning = FinancialPlanningFactory(cdi=0.1213, ipca=0.0750)

        self.reserve_in_lack = ReserveInLackFactory(
                               financial_planning=financial_planning,
                               value_0_to_24_mounth=13000,
                               value_24_to_60_mounth=10000,
                               value_60_to_120_mounth=5000,
                               value_120_to_240_mounth=5000)

    def test_patrimony_necessery_in_period(self):
        self.assertAlmostEqual(
            self.reserve_in_lack.patrimony_necessery_in_period(
                24, 13000), 192124.8373901789)

    def test_patrimony_necessery_total(self):
        self.assertAlmostEqual(self.reserve_in_lack.
                               patrimony_necessery_total(), 595624.31498015427)


class ProtectionManagerTest(TestCase):

    def setUp(self):
        active_client = ActiveClientMainFactory(
            birthday=datetime.datetime(1967, 1, 1))
        financial_planning = FinancialPlanningFactory(
            cdi=0.1213, ipca=0.075, active_client=active_client)
        self.protection_manager = financial_planning.protection_manager
        self.protection_manager.financial_planning.active_client =\
            active_client
        self.protection_manager.private_pensions.all().update(
            accumulated=20000, value_annual=2000)
        PrivatePensionFactory(protection_manager=self.protection_manager,
                              accumulated=4000, value_annual=200)
        for life_insurance in self.protection_manager.life_insurances.all():
            life_insurance.delete()

        life_insurances = [
            {'value_to_pay_annual': 2000, 'has_year_end': False,
                'value_to_recive': 500000, 'actual': True},
            {'value_to_pay_annual': 2000, 'has_year_end': True,
                'year_end': 2020, 'value_to_recive': 200000, 'actual': False},
            {'value_to_pay_annual': 1000, 'has_year_end': True,
                'year_end': 2023, 'value_to_recive': 300000, 'actual': True}]

        for life_insurance in life_insurances:
            LifeInsuranceFactory(**life_insurance,
                                 protection_manager=self.protection_manager)

    def test_life_insurances_flow(self):
        data = [5000.0, 5000.0, 5000.0, 5000.0, 3000.0, 3000.0, 3000.0, 2000.0,
                2000.0, 2000.0]
        self.assertEqual(self.protection_manager.life_insurances_flow(), data)


class ActualPatrimonyProtectionTest(TestCase):

    def setUp(self):
        financial_planning = FinancialPlanningFactory()
        reserve_in_lack = ReserveInLackFactory(financial_planning=\
                                                financial_planning)
        self.actual_patrimony_protection = ActualPatrimonyProtectionFactory(
                                            reserve_in_lack=reserve_in_lack)
        independence_patrimony_protection =\
                IndependencePatrimonyProtectionFactory(
                                            reserve_in_lack=reserve_in_lack)

        for private_pension in self.actual_patrimony_protection.\
                                    private_pensions.all():
            private_pension.delete()

        private_pensions = [
            {'accumulated': 20000, 'value_annual': 2000},
            {'accumulated': 4000, 'value_annual': 200},
        ]

        for private_pension in private_pensions:
            PrivatePensionFactory(**private_pension,
                                      actual_patrimony_protection=\
                                      self.actual_patrimony_protection,
                                      independence_patrimony_protection=\
                                      independence_patrimony_protection)

        for life_insurance in self.actual_patrimony_protection.\
                              life_insurances.all():
            life_insurance.delete()

        life_insurances = [
            {'value_to_pay_annual': 2000, 'value_to_recive': 500000,
                'actual': True},
            {'value_to_pay_annual': 2000, 'value_to_recive': 200000,
                'actual': False},
            {'value_to_pay_annual': 1000, 'value_to_recive': 300000,
                'actual': True}
        ]

        for life_insurance in life_insurances:
            LifeInsuranceFactory(**life_insurance,
                                         actual_patrimony_protection=self.\
                                         actual_patrimony_protection,)

    def test_private_pension_total(self):
        self.assertEqual(self.actual_patrimony_protection.\
                           private_pension_total(), 24000)

    def test_dont_have_life_insurance(self):
        for life_insurance in self.actual_patrimony_protection.\
                              life_insurances.all():
            life_insurance.delete()
        self.assertEqual(self.actual_patrimony_protection.
                         life_insurance_to_recive_total(), 0)

    def test_life_insurance_to_recive_total(self):
        self.assertEqual(self.actual_patrimony_protection.\
                         life_insurance_to_recive_total(), 800000)

class IndependencePatrimonyProtectionTest(TestCase):

    def setUp(self):
        active_client = ActiveClientMainFactory(
            birthday=datetime.datetime(1967, 1, 1))
        financial_planning = FinancialPlanningFactory(active_client=\
                                                    active_client, ipca=0.075)
        reserve_in_lack = ReserveInLackFactory(financial_planning=\
                                                financial_planning)
        actual_patrimony_protection = ActualPatrimonyProtectionFactory(
                                            reserve_in_lack=reserve_in_lack)
        self.independence_patrimony_protection =\
                IndependencePatrimonyProtectionFactory(
                                            reserve_in_lack=reserve_in_lack)

        for private_pension in self.independence_patrimony_protection.\
                                    private_pensions.all():
            private_pension.delete()

        for life_insurance in self.independence_patrimony_protection.\
                              life_insurances.all():
            life_insurance.delete()

        private_pensions = [
            {'accumulated': 20000, 'value_annual': 2000, 'rate': 0.1213},
            {'accumulated': 4000, 'value_annual': 200, 'rate': 0.09},
            {'accumulated': 4000, 'value_annual': 200, 'rate': 0.09},
        ]

        self.private_pensions_array = []

        for private_pension in private_pensions:
            element = PrivatePensionFactory(**private_pension,
                                  independence_patrimony_protection=\
                                  self.independence_patrimony_protection,
                                  actual_patrimony_protection=\
                                  actual_patrimony_protection)
            self.private_pensions_array.append(element)

        life_insurances = [
            {'value_to_pay_annual': 2000, 'value_to_recive': 500000,
                'actual': True},
            {'value_to_pay_annual': 2000, 'value_to_recive': 200000,
                'actual': False},
            {'value_to_pay_annual': 1000, 'value_to_recive': 300000,
                'actual': True}
        ]

        for life_insurance in life_insurances:
            LifeInsuranceFactory(**life_insurance,
                                  independence_patrimony_protection=\
                                  self.independence_patrimony_protection,
                                  actual_patrimony_protection=\
                                  actual_patrimony_protection)

    def test_private_pension_total(self):
        self.assertAlmostEqual(
            self.independence_patrimony_protection.\
                    private_pension_total(), 68297.050164)

    def test_private_pension_individual(self):
        self.assertAlmostEqual(self.private_pensions_array[0].\
                accumulated_moniterized(), 54847.2658609)

    def test_dont_have_life_insurance(self):
        for life_insurance in self.independence_patrimony_protection.\
                              life_insurances.all():
            life_insurance.delete()
        self.assertEqual(self.independence_patrimony_protection.
                         life_insurance_to_recive_total(), 0)

    def test_life_insurance_to_recive_total(self):
        self.assertEqual(self.independence_patrimony_protection.\
                          life_insurance_to_recive_total(), 1000000)
