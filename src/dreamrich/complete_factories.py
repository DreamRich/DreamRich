""" Centralized complete factories to avoid cyclic imports problems
"""
import factory
from client.factories import (
    ActiveClientFactory,
    AddressFactory,
    BankAccountFactory,
    ClientFactory,
    DependentFactory,
)
from financial_planning.factories import (
    CostManagerFactory,
    FinancialIndependenceFactory,
    FinancialPlanningFactory,
)
from patrimony.factories import (
    ActiveFactory,
    ActiveManagerFactory,
    ArrearageFactory,
    CompanyParticipationFactory,
    EquipmentFactory,
    IncomeFactory,
    MovablePropertyFactory,
    PatrimonyFactory,
    RealEstateFactory,
)
from protection.factories import (
    ActualPatrimonySuccessionFactory,
    EmergencyReserveFactory,
    IndependencePatrimonySuccessionFactory,
    LifeInsuranceFactory,
    PrivatePensionFactory,
    ProtectionManagerFactory,
    ReserveInLackFactory
)
from goal.factories import GoalManagerFactory


class ActiveManagerCompleteFactory(ActiveManagerFactory):

    actives = factory.RelatedFactory(
        ActiveFactory,
        'active_manager'
    )


class PatrimonyCompleteFactory(PatrimonyFactory):

    active_manager = factory.RelatedFactory(
        ActiveManagerCompleteFactory,
        'patrimony'
    )
    emergency_reserve = factory.RelatedFactory(
        EmergencyReserveFactory,
        'patrimony'
    )

    arrearages = factory.RelatedFactory(
        ArrearageFactory,
        'patrimony'
    )
    real_estates = factory.RelatedFactory(
        RealEstateFactory,
        'patrimony'
    )
    equipments = factory.RelatedFactory(
        EquipmentFactory,
        'patrimony'
    )
    incomes = factory.RelatedFactory(
        IncomeFactory,
        'patrimony'
    )
    movable_properties = factory.RelatedFactory(
        MovablePropertyFactory,
        'patrimony'
    )
    emergency_reserve = factory.RelatedFactory(
       EmergencyReserveFactory,
       'patrimony'
    )
    company_participations = factory.RelatedFactory(
        CompanyParticipationFactory,
        'patrimony'
    )


class EmergencyReserveCompleteFactory(EmergencyReserveFactory):

    patrimony = factory.RelatedFactory(
        PatrimonyCompleteFactory,
        'emergency_reserve'
    )
    cost_manager = factory.RelatedFactory(
        CostManagerFactory,
        'emergency_reserve'
    )


class ProtectionManagerCompleteFactory(ProtectionManagerFactory):

    reserve_in_lack = factory.RelatedFactory(
        ReserveInLackFactory,
        'protection_manager'
    )

    actual_patrimony_succession = factory.RelatedFactory(
        ActualPatrimonySuccessionFactory,
        'protection_manager'
    )

    future_patrimony_succession = factory.RelatedFactory(
        IndependencePatrimonySuccessionFactory,
        'protection_manager'
    )

    private_pensions = factory.RelatedFactory(
        PrivatePensionFactory,
        'protection_manager'
    )

    life_insurance = factory.RelatedFactory(
        LifeInsuranceFactory,
        'protection_manager'
    )


class FinancialPlanningCompleteFactory(FinancialPlanningFactory):

    patrimony = factory.RelatedFactory(
        PatrimonyCompleteFactory,
        'financial_planning'
    )
    cost_manager = factory.RelatedFactory(
        CostManagerFactory,
        'financial_planning'
    )

    financial_independence = factory.RelatedFactory(
        FinancialIndependenceFactory,
        'financial_planning'
    )

    protection_manager = factory.RelatedFactory(
        ProtectionManagerCompleteFactory,
        'financial_planning'
    )

    goal_manager = factory.RelatedFactory(
        GoalManagerFactory,
        'financial_planning'
    )


class ActiveClientCompleteFactory(ActiveClientFactory):

    financial_planning = factory.RelatedFactory(
        FinancialPlanningCompleteFactory,
        'active_client'
    )

    spouse = factory.RelatedFactory(
        ClientFactory,
        'active_spouse'
    )

    dependents = factory.RelatedFactory(
        DependentFactory,
        'active_client'
    )

    bank_account = factory.RelatedFactory(
        BankAccountFactory,
        'active_client'
    )

    addresses = factory.RelatedFactory(
        AddressFactory,
        'active_client'
    )
