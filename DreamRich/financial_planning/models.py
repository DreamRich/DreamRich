from django.db import models
from client.models import ActiveClient
from patrimony.models import Patrimony
from goal.models import GoalManager


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()


class RegularCost(models.Model):

    home = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    electricity_bill = models.DecimalField(decimal_places=2, max_digits=8,
                                           default=0)
    gym = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    taxes = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    car_gas = models.DecimalField(decimal_places=2, max_digits=8, default=0)

    insurance = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    cellphone = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    health_insurance = models.DecimalField(decimal_places=2, max_digits=8,
                                           default=0)
    supermarket = models.DecimalField(decimal_places=2, max_digits=8,
                                      default=0)
    housekeeper = models.DecimalField(decimal_places=2, max_digits=8,
                                      default=0)
    beauty = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    internet = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    netflix = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    recreation = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    meals = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    appointments = models.DecimalField(
        decimal_places=2, max_digits=8, default=0)  # consultas
    drugstore = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    extras = models.DecimalField(decimal_places=2, max_digits=8, default=0)

    @property
    def total(self):
        total = self.home + self.electricity_bill + self.gym + self.taxes \
            + self.car_gas + self.insurance + self.cellphone \
            + self.health_insurance + self.supermarket + self.housekeeper \
            + self.beauty + self.internet + self.netflix + self.recreation \
            + self.meals + self.appointments + self.drugstore + self.extras

        return total


class FinancialPlanning(models.Model):

    active_client = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    patrimony = models.OneToOneField(
        Patrimony,
        on_delete=models.CASCADE,
    )

    financial_independence = models.OneToOneField(
        FinancialIndependence,
        on_delete=models.CASCADE,
    )

    goal_manager = models.OneToOneField(
        GoalManager,
        on_delete=models.CASCADE,
    )

    regular_cost = models.OneToOneField(
        RegularCost,
        on_delete=models.CASCADE)
