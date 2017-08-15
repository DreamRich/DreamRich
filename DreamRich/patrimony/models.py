from django.db import models


class Active(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8) 

class Arrearage(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8) 

class RealEstate(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8) 
    salable = models.BooleanField()

class CompanyParticipation(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8) 

class Equipment(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8) 

class LifeInsurance(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8) 
    redeemable = models.BooleanField()

class Income(models.Model):
    source = models.CharField(max_length = 100)
    value_monthly = models.DecimalField(decimal_places = 2, max_digits = 8) 
    thirteenth = models.DecimalField(decimal_places = 2, max_digits = 8) 
    vacation = models.DecimalField(decimal_places = 2, max_digits = 8) 

class Patrimony(models.Model):
    fgts = models.DecimalField(decimal_places = 2, max_digits = 8)
    active = models.ForeignKey(Active, on_delete=models.CASCADE, default=0)
    arrearage = models.ForeignKey(Arrearage, on_delete=models.CASCADE, default=0)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    compant_participation = models.ForeignKey(CompanyParticipation, on_delete=models.CASCADE, default=0)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
