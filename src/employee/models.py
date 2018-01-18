from django.db import models
from dreamrich import validators
from dr_auth.models import BaseUser
from dr_auth.models_permissions import (
    EMPLOYEE_MODEL_PERMISSIONS,
    EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS,
    FINANCIAL_ADVISER_MODEL_PERMISSIONS,
    FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS
)


class Employee(BaseUser):

    class Meta:
        permissions = EMPLOYEE_MODEL_PERMISSIONS

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )

    default_permissions_codenames = EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS


class FinancialAdviser(Employee):

    class Meta:
        permissions = FINANCIAL_ADVISER_MODEL_PERMISSIONS

    clients = models.ManyToManyField(
        'client.ActiveClient',
        related_name='financial_advisers'
    )

    default_permissions_codenames = \
        FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS
