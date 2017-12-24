from django.db import models
from django.contrib.auth.models import Permission
from dreamrich import validators
from client.models import ActiveClient
from dr_auth.models import BaseUser


class Employee(BaseUser):

    class Meta:
        permissions = (
            ('see_employee', 'Obrigatory for user can see any employee'),
            ('see_own_employee', 'See own employees (or itself, if employee)'),
            ('see_other_employee', 'See other employees (or not yours)'),
            ('see_employee_list', 'See list of employees itself'),

            ('add_employee', 'Create an employee'),

            ('change_employee', 'Obrigatory for user can change any employee'),
            ('change_own_employee', 'Change own employees (or itself)'),
            ('change_other_employee', 'See other employees (or not yours)'),

            ('delete_employee', 'Obrigatory for user can change any employee'),
            ('delete_other_employee', 'Delete other employees (or not yours)'),
        )

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )

    # To facilitate getting default permissions in others places
    @property
    def default_permissions(self):
        permissions_codenames = [
            'see_client', 'delete_client',
            'see_other_client', 'add_client'

            'see_employee', 'change_employee',
            'see_own_employee', 'change_own_employee'
        ]

        permissions = []
        for permission_codename in permissions_codenames:
            permissions += \
                [Permission.objects.get(codename=permission_codename)]

        return permissions


class FinancialAdviser(Employee):

    clients = models.ManyToManyField(
        ActiveClient,
        related_name='financial_advisers'
    )
