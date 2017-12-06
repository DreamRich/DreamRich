import datetime
from django.db import models
from patrimony.models import Patrimony
from django.db.models import Sum
import numpy
import abc


class ReserveInLack(models.Model):

    value_0_to_24_mounth = models.PositiveSmallIntegerField()

    value_24_to_60_mounth = models.PositiveSmallIntegerField()

    value_60_to_120_mounth = models.PositiveSmallIntegerField()

    value_120_to_240_mounth = models.PositiveSmallIntegerField()

    def patrimony_necessery_in_period(self, mounth_quantities, value):
        rate = self.protection_manager.financial_planning.real_gain()
        return numpy.pv(rate, mounth_quantities, -value)

    def patrimony_necessery_total(self):
        portion_0_to_24_mounth = self.patrimony_necessery_in_period(
            24, self.value_0_to_24_mounth)
        portion_24_to_60_mounth = self.patrimony_necessery_in_period(
            36, self.value_24_to_60_mounth)
        portion_60_to_120_mounth = self.patrimony_necessery_in_period(
            60, self.value_60_to_120_mounth)
        portion_120_to_240_mounth = self.patrimony_necessery_in_period(
            120, self.value_120_to_240_mounth)

        total = portion_0_to_24_mounth + portion_24_to_60_mounth +\
            portion_60_to_120_mounth + portion_120_to_240_mounth

        return total


class EmergencyReserve(models.Model):

    mounth_of_protection = models.PositiveSmallIntegerField()

    def necessery_value(self):
        regular_cost_mounthly = self.protection_manager.financial_planning.\
            cost_manager.total()
        total = self.mounth_of_protection * regular_cost_mounthly

        return total

    def risk_gap(self):
        current_patrimony = self.protection_manager.financial_planning.\
            patrimony.current_net_investment()
        necessery_value = self.necessery_value()
        if current_patrimony < necessery_value:
            total = necessery_value - current_patrimony
        else:
            total = 0

        return total


class ProtectionManager(models.Model):

    reserve_in_lack = models.OneToOneField(
        ReserveInLack,
        on_delete=models.CASCADE,
        related_name='protection_manager',
    )

    emergency_reserve = models.OneToOneField(
        EmergencyReserve,
        on_delete=models.CASCADE,
        related_name='protection_manager',
    )

    def private_pension_total(self):
        total = self.private_pensions.aggregate(Sum('accumulated'))
        total = (total['accumulated__sum'] or 0)

        return total

    def life_insurances_flow(self):
        duration_flow = self.financial_planning.duration()
        data = [0] * duration_flow
        life_insurances = self.life_insurances.all()

        for life_insurance in life_insurances:
            for index in range(duration_flow):
                if life_insurance.index_end() >= index:
                    data[index] += life_insurance.value_to_pay_annual

        return data

    def private_pension_total_in_independece(self):
        actual_accumulated = self.private_pension_total()
        total_value = self.private_pensions.aggregate(Sum('value_annual'))
        total_value = (total_value['value_annual__sum'] or 0)
        rate = self.financial_planning.real_gain()
        duration = self.financial_planning.duration()
        total_value_moniterized = numpy.fv(rate, duration, -total_value,
                                           -actual_accumulated)

        return total_value_moniterized

    def life_insurance_to_recive_total(self):
        value = self.life_insurances.filter(actual=True).aggregate(Sum(
                                     'value_to_recive'))
        value = (value['value_to_recive__sum'] or 0)

        return value

    def life_insurance_to_recive_in_independence(self):
        value = self.life_insurances.aggregate(Sum('value_to_recive'))
        value = (value['value_to_recive__sum'] or 0)

        return value


class SuccessionTemplate(models.Model):

    class Meta:
        abstract = True

    __metaclass__ = abc.ABCMeta
    itcmd_tax = models.FloatField(default=0)
    oab_tax = models.FloatField(default=0)
    other_taxes = models.FloatField(default=0)
    reserve_in_lack = models.OneToOneField(
        ReserveInLack,
        on_delete=models.CASCADE,
    )

    @abc.abstractmethod
    def private_pension_total(self):
        """Calculate total private pension"""
        pass

    @abc.abstractmethod
    def life_insurance_to_recive_total(self):
        """Calculate total life_insurance to recive"""
        pass

    @abc.abstractmethod
    def patrimony_total(self):
        """Recover the total patrimony in respective period"""
        pass

    def patrimony_necessery_to_itcmd(self):
        total = self.patrimony_total() * self.itcmd_tax

        return total

    def patrimony_necessery_to_oab(self):
        total = self.patrimony_total() * self.oab_tax

        return total

    def patrimony_necessery_to_other_taxes(self):
        total = self.patrimony_total() * self.other_taxes

        return total

    def patrimony_necessery_total_to_sucession(self):
        total = self.patrimony_necessery_to_itcmd() +\
                self.patrimony_necessery_to_oab() +\
                self.patrimony_necessery_to_other_taxes()

        return total

    def total_to_recive_after_death_without_taxes(self):
        total = self.private_pension_total() +\
                self.life_insurance_to_recive_total()

        return total

    def leftover_after_sucession(self):
        total = self.total_to_recive_after_death_without_taxes() -\
                self.patrimony_necessery_total_to_sucession()

        return total

    def need_for_vialicia(self):
        total = self.leftover_after_sucession() +\
                self.patrimony_total() -\
                self.reserve_in_lack.patrimony_necessery_total()


class ActualPatrimonyProtection(SuccessionTemplate):

    patrimony = models.OneToOneField(Patrimony, on_delete=models.CASCADE)

    def private_pension_total(self):
        total = self.private_pensions.aggregate(Sum('accumulated'))
        total = (total['accumulated__sum'] or 0)

        return total

    def life_insurance_to_recive_total(self):
        value = self.life_insurances.filter(actual=True).aggregate(Sum(
                                     'value_to_recive'))
        value = (value['value_to_recive__sum'] or 0)

        return value

    def patrimony_total(self):
        return self.patrimony.total()


class PrivatePension(models.Model):
    name = models.CharField(max_length=100)
    value_annual = models.FloatField(default=0)
    accumulated = models.FloatField(default=0)
    protection_manager = models.ForeignKey(
        ProtectionManager,
        on_delete=models.CASCADE,
        related_name='private_pensions')
    actual_patrimony_protection = models.ForeignKey(
        ActualPatrimonyProtection,
        on_delete=models.CASCADE,
        related_name='private_pensions')

    def __str__(self):
        return "{name} {value_annual} {accumulated}".format(**self.__dict__)


class LifeInsurance(models.Model):
    name = models.CharField(max_length=100)
    value_to_recive = models.FloatField(default=0)
    value_to_pay_annual = models.FloatField(default=0)
    year_end = models.PositiveSmallIntegerField(null=True)
    redeemable = models.BooleanField()
    actual = models.BooleanField()
    has_year_end = models.BooleanField()
    protection_manager = models.ForeignKey(
        ProtectionManager,
        on_delete=models.CASCADE,
        related_name='life_insurances')
    actual_patrimony_protection = models.ForeignKey(
        ActualPatrimonyProtection,
        on_delete=models.CASCADE,
        related_name='life_insurances')

    def index_end(self):
        if self.has_year_end:
            actual_year = datetime.datetime.now().year
            index = self.year_end - actual_year
        else:
            index = self.protection_manager.financial_planning.duration()

        return index

    def __str__(self):
        string = "{name} {value_to_pay_annual} {value_to_recive}"
        return string.format(**self.__dict__)
