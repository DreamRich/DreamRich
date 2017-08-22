from django.db import models
from dreamrich import validators
from client.models import ActiveClient
from django.contrib.auth.models import User


class Employee(User):
    name = models.CharField(
        max_length=30
    )

    surname = models.CharField(
        max_length=30
    )

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_CPF]
    )

class FinancialAdviser(Employee):
    clients = models.ManyToManyField(ActiveClient)
