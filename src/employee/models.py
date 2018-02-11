from django.db import models
from dreamrich import validators
from dr_auth.models import BaseUser
from dr_auth.models_permissions import (
    get_formatted_permissions,
    USERS_PERMISSIONS_INFO
)


class Employee(BaseUser):

    class Meta:
        permissions = get_formatted_permissions(
            USERS_PERMISSIONS_INFO.employee.nick
        )

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )

    default_permissions_codenames = \
        USERS_PERMISSIONS_INFO.employee.default_codenames


class FinancialAdviser(Employee):

    class Meta:
        permissions = get_formatted_permissions(
            USERS_PERMISSIONS_INFO.financial_adviser.nick
        )

    clients = models.ManyToManyField(
        'client.ActiveClient',
        related_name='financial_advisers'
    )

    default_permissions_codenames = \
        USERS_PERMISSIONS_INFO.financial_adviser.default_codenames
