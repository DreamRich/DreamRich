from django.db import models
from dreamrich import validators
from client.models import ActiveClient
from dr_auth.models import BaseUser


class Employee(BaseUser):
    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )

    def save(self, *args, **kwargs):
        self.full_clean()
 
        super(Employee, self).save(*args, **kwargs)

class FinancialAdviser(Employee):
    clients = models.ManyToManyField(ActiveClient)

