from django.db import models

class ReserveInLack(models.Model):

    value_0_to_24_mounth = models.PositiveSmallIntegerField()
    value_24_to_60_mounth = models.PositiveSmallIntegerField()
    value_60_to_120_mounth = models.PositiveSmallIntegerField()
    value_120_to_240_mounth = models.PositiveSmallIntegerField()

class EmergencyReserve(models.Model):

    mounth_of_protection = models.PositiveSmallIntegerField()
