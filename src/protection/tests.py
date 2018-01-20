import datetime
from django.test import TestCase
from protection.factories import (
    PrivatePensionFactory,
    LifeInsuranceFactory
)
from financial_planning.factories import RegularCostFactory
from dreamrich.complete_factories import (
    ActiveClientCompleteFactory,
    FinancialPlanningCompleteFactory,
    PatrimonyCompleteFactory,
    ProtectionManagerCompleteFactory
)
from client.factories import ActiveClientFactory
from patrimony.factories import ActiveFactory


def _create_reserve_in_lack():
    active_client = ActiveClientCompleteFactory()

    financial_planning = FinancialPlanningCompleteFactory(
        cdi=0.1213,
        ipca=0.0750
    )

    active_client.financial_planning = financial_planning

    protection_manager = financial_planning.protection_manager

    reserve_in_lack = protection_manager.reserve_in_lack
    reserve_in_lack.value_0_to_24_month = 13000
    reserve_in_lack.value_24_to_60_month = 10000
    reserve_in_lack.value_60_to_120_month = 5000
    reserve_in_lack.value_120_to_240_month = 5000

    return reserve_in_lack


class EmergencyReserveTest(TestCase):

    def setUp(self):
        patrimony = PatrimonyCompleteFactory()

        self.emergency_reserve = patrimony.emergency_reserve
        self.emergency_reserve.month_of_protection = 12

        self.active_manager = patrimony.active_manager

        for active in self.active_manager.actives.all():
            active.delete()

        cost_manager = self.emergency_reserve.cost_manager

        for regular_cost in cost_manager.regular_costs.all():
            regular_cost.delete()

        for arrearage in patrimony.arrearages.all():
            arrearage.delete()

        regular_costs = [{'value': 500}, {'value': 1500}, {'value': 2500}]

        for regular_cost in regular_costs:
            RegularCostFactory(**regular_cost, cost_manager=cost_manager)

    def test_necessary_value(self):
        self.assertEqual(self.emergency_reserve.necessary_value(), 54000)

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
        self.reserve_in_lack = _create_reserve_in_lack()

    def test_patrimony_necessary_in_period(self):
        self.assertAlmostEqual(
            self.reserve_in_lack.patrimony_necessary_in_period(24, 13000),
            192124.8373901789
        )

    def test_patrimony_necessary_total(self):
        self.assertAlmostEqual(
            self.reserve_in_lack.
            patrimony_necessary_total(),
            595624.31498015427
        )


class ProtectionManagerTest(TestCase):

    def setUp(self):
        active_client = ActiveClientCompleteFactory(
            birthday=datetime.datetime(1967, 1, 1)
        )

        active_client.financial_planning.cdi = 0.1213
        active_client.financial_planning.ipca = 0.1213

        self.protection_manager = \
            active_client.financial_planning.protection_manager

        self.protection_manager.private_pensions.all().update(
            value=20000, annual_investment=2000
        )

        for life_insurance in self.protection_manager.life_insurances.all():
            life_insurance.delete()

        for private_pension in self.protection_manager.private_pensions.all():
            private_pension.delete()

        life_insurances = [
            {'value_to_pay_annual': 2000, 'has_year_end': False},
            {'value_to_pay_annual': 2000, 'has_year_end': True,
                'year_end': 2020, },
            {'value_to_pay_annual': 1000, 'has_year_end': True,
                'year_end': 2023, }]

        for life_insurance in life_insurances:
            LifeInsuranceFactory(**life_insurance,
                                 protection_manager=self.protection_manager)

        private_pensions = [
            {'annual_investment': 5000}, {'annual_investment': 3000},
            {'annual_investment': 2000}, {'annual_investment': 8000},
        ]

        for private_pension in private_pensions:
            PrivatePensionFactory(protection_manager=self.protection_manager,
                                  **private_pension)

    def test_life_insurances_flow(self):
        data = [5000.0, 5000.0, 5000.0, 5000.0, 3000.0, 3000.0, 3000.0, 2000.0,
                2000.0, 2000.0]
        self.assertEqual(self.protection_manager.life_insurances_flow(), data)

    def test_private_pensions_total(self):
        self.assertEqual(self.protection_manager.private_pensions_total(),
                         18000)

    def test_flow(self):
        data = [23000.0, 23000.0, 23000.0, 23000.0, 21000.0, 21000.0, 21000.0,
                20000.0, 20000.0, 20000.0]
        self.assertEqual(self.protection_manager.flow(), data)


class ActualPatrimonySuccessionTest(TestCase):

    def setUp(self):
        reserve_in_lack = _create_reserve_in_lack()
        protection_manager = reserve_in_lack.protection_manager

        for private_pension in protection_manager.private_pensions.all():
            private_pension.delete()

        for life_insurance in protection_manager.life_insurances.all():
            life_insurance.delete()

        private_pensions = [
            {'value': 20000, 'annual_investment': 2000},
            {'value': 4000, 'annual_investment': 200},
        ]

        for private_pension in private_pensions:
            new_private_pension = PrivatePensionFactory(**private_pension)
            protection_manager.private_pensions.add(new_private_pension)

        life_insurances = [
            {'value_to_pay_annual': 2000, 'value_to_recive': 500000,
                'actual': True},
            {'value_to_pay_annual': 2000, 'value_to_recive': 200000,
                'actual': False},
            {'value_to_pay_annual': 1000, 'value_to_recive': 300000,
                'actual': True}
        ]

        for life_insurance in life_insurances:
            new_life_insurance = LifeInsuranceFactory(**life_insurance)
            protection_manager.life_insurances.add(new_life_insurance)

        self.actualpatrimonysuccession = protection_manager.\
            actualpatrimonysuccession
        self.actualpatrimonysuccession.itcmd_tax = 0.06
        self.actualpatrimonysuccession.oab_tax = 0.05
        self.actualpatrimonysuccession.other_taxes = 0.02
        self.protection_manager = protection_manager

    def test_private_pension_total(self):
        self.assertEqual(self.actualpatrimonysuccession.
                         private_pension_total(), 24000)

    def test_dont_have_life_insurance(self):
        for life_insurance in self.protection_manager.life_insurances.all():
            life_insurance.delete()
        self.assertEqual(self.actualpatrimonysuccession.
                         life_insurance_to_recive_total(), 0)

    def test_life_insurance_to_recive_total(self):
        self.assertEqual(self.actualpatrimonysuccession.
                         life_insurance_to_recive_total(), 800000)

    def test_patrimony_total(self):
        self.assertAlmostEqual(self.actualpatrimonysuccession.
                               patrimony_total(), 322788.03)

    def test_patrimony_necessary_to_itcmd(self):
        self.assertAlmostEqual(self.actualpatrimonysuccession.
                               patrimony_necessary_to_itcmd(), 19367.2818)

    def test_patrimony_necessary_to_itcmd_with_joint_account(self):
        self.actualpatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(self.actualpatrimonysuccession.
                               patrimony_necessary_to_itcmd(), 9683.6409)

    def test_patrimony_necessary_to_oab(self):
        self.assertAlmostEqual(
            self.actualpatrimonysuccession.
            patrimony_necessary_to_oab(),
            16139.401500000002)

    def test_patrimony_necessary_to_oab_with_joint_account(self):
        self.actualpatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(
            self.actualpatrimonysuccession.
            patrimony_necessary_to_oab(),
            8069.700750000001)

    def test_patrimony_necessary_to_other_taxes(self):
        self.assertAlmostEqual(
            self.actualpatrimonysuccession.
            patrimony_necessary_to_other_taxes(),
            6455.7606000000005)

    def test_patrimony_necessary_to_other_taxes_joint_account(self):
        self.actualpatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(
            self.actualpatrimonysuccession.
            patrimony_necessary_to_other_taxes(),
            3227.8803000000003)

    def test_patrimony_necessary_total_to_sucession(self):
        self.assertAlmostEqual(
            self.actualpatrimonysuccession.
            patrimony_necessary_total_to_sucession(),
            41962.443900000006)

    def test_patrimony_necessary_to_sucession_joint_account(self):
        self.actualpatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(
            self.actualpatrimonysuccession.
            patrimony_necessary_total_to_sucession(),
            20981.221950000003)

    def test_total_to_recive_after_death_without_taxes(self):
        self.assertEqual(self.actualpatrimonysuccession.
                         total_to_recive_after_death_without_taxes(), 824000)

    def test_leftover_after_sucession(self):
        self.assertAlmostEqual(self.actualpatrimonysuccession.
                               leftover_after_sucession(), 782037.5561)

    def test_need_for_vialicia(self):
        self.assertAlmostEqual(self.actualpatrimonysuccession.
                               need_for_vialicia(), 509201.2711198457)


class IndependencePatrimonySuccessionTest(TestCase):

    def setUp(self):
        active_client = ActiveClientCompleteFactory(
            birthday=datetime.datetime(1967, 1, 1)
        )
        active_client.financial_planning.ipca = 0.075

        reserve_in_lack = _create_reserve_in_lack()
        protection_manager = reserve_in_lack.protection_manager
        protection_manager.financial_planning = \
            active_client.financial_planning

        for private_pension in protection_manager.private_pensions.all():
            private_pension.delete()

        for life_insurance in protection_manager.life_insurances.all():
            life_insurance.delete()

        private_pensions = [
            {'value': 20000, 'annual_investment': 2000, 'rate': 0.1213},
            {'value': 4000, 'annual_investment': 200, 'rate': 0.09},
            {'value': 4000, 'annual_investment': 200, 'rate': 0.09},
        ]

        self.private_pensions_array = []

        for private_pension in private_pensions:
            element = PrivatePensionFactory(
                **private_pension, protection_manager=protection_manager)
            self.private_pensions_array.append(element)

        life_insurances = [
            {'value_to_pay_annual': 2000, 'value_to_recive': 500000,
                'actual': True},
            {'value_to_pay_annual': 2000, 'value_to_recive': 200000,
                'actual': False},
            {'value_to_pay_annual': 1000, 'value_to_recive': 300000,
                'actual': True},
            {'value_to_pay_annual': 1000, 'value_to_recive': 300000,
                'actual': True},
        ]

        for life_insurance in life_insurances:
            LifeInsuranceFactory(**life_insurance,
                                 protection_manager=protection_manager)

        self.independencepatrimonysuccession =\
            protection_manager.independencepatrimonysuccession
        self.independencepatrimonysuccession.itcmd_tax = 0.06
        self.independencepatrimonysuccession.oab_tax = 0.05
        self.independencepatrimonysuccession.other_taxes = 0.02
        self.protection_manager = protection_manager

    def test_private_pension_total(self):
        self.assertAlmostEqual(self.independencepatrimonysuccession.
                               private_pension_total(), 68297.050164)

    def test_private_pension_individual(self):
        self.assertAlmostEqual(self.private_pensions_array[0].
                               value_moniterized(), 54847.2658609)

    def test_dont_have_life_insurance(self):
        for life_insurance in self.protection_manager.life_insurances.all():
            life_insurance.delete()
        self.assertEqual(self.independencepatrimonysuccession.
                         life_insurance_to_recive_total(), 0)

    def test_life_insurance_to_recive_total(self):
        self.assertEqual(self.independencepatrimonysuccession.
                         life_insurance_to_recive_total(), 1300000)

    def test_patrimony_total(self):
        self.assertEqual(self.independencepatrimonysuccession.patrimony_total(),
                         9054063.57430404)

    def test_patrimony_necessary_to_itcmd(self):
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.patrimony_necessary_to_itcmd(),
            543243.8144582424)

    def test_patrimony_necessary_to_itcmd_with_joint_account(self):
        self.independencepatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(self.independencepatrimonysuccession.
                               patrimony_necessary_to_itcmd(),
                               271621.9072291212)

    def test_patrimony_necessary_to_oab(self):
        self.assertAlmostEqual(self.independencepatrimonysuccession.
                               patrimony_necessary_to_oab(), 452703.178715202)

    def test_patrimony_necessary_to_oab_with_joint_account(self):
        self.independencepatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.
            patrimony_necessary_to_oab(),
            226351.589357601)

    def test_patrimony_necessary_to_other_taxes(self):
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.
            patrimony_necessary_to_other_taxes(),
            181081.2714860808)

    def test_patrimony_necessary_to_other_taxes_joint_account(self):
        self.independencepatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.
            patrimony_necessary_to_other_taxes(),
            90540.6357430404)

    def test_patrimony_necessary_total_to_sucession(self):
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.
            patrimony_necessary_total_to_sucession(),
            1177028.2646595251)

    def test_patrimony_necessary_to_sucession_joint_account(self):
        self.independencepatrimonysuccession.protection_manager.\
            financial_planning.active_client.bank_account.joint_account = True
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.
            patrimony_necessary_total_to_sucession(),
            588514.1323297626)

    def test_total_to_recive_after_death_without_taxes(self):
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.
            total_to_recive_after_death_without_taxes(),
            1368297.0501640132)

    def test_leftover_after_sucession(self):
        self.assertAlmostEqual(self.independencepatrimonysuccession.
                               leftover_after_sucession(), 191268.78550448804)

    def test_need_for_vialicia(self):
        self.assertAlmostEqual(
            self.independencepatrimonysuccession.need_for_vialicia(),
            8649708.0448283739)


class PrivatePensionTest(TestCase):

    def setUp(self):
        protection_manager = ProtectionManagerCompleteFactory()
        self.private_pension = protection_manager.private_pensions.first()

    def test_active_type_when_create(self):
        self.assertEqual(self.private_pension.active_type.name, 'PREVIDÊNCIA')

    def test_active_type_if_deleted(self):
        self.private_pension.active_type.delete()
        self.assertEqual(self.private_pension.active_type.name, 'PREVIDÊNCIA')

    def test_active_type_if_deleted_and_save(self):
        self.private_pension.active_type.delete()
        self.private_pension.active_type.save()
        self.assertEqual(self.private_pension.active_type.name, 'PREVIDÊNCIA')

    def test_active_type_if_changed_name(self):
        self.private_pension.active_type.name = 'Other name'
        self.private_pension.save()
        self.assertEqual(self.private_pension.active_type.name, 'PREVIDÊNCIA')
