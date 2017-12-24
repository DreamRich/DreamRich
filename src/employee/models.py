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

    class Meta:
        # fa = financial adviser
        permissions = (
            ('see_fa', 'Obrigatory for user can see any fa'),
            ('see_own_fa', 'See own fas (or itself, if fa)'),
            ('see_other_fa', 'See other fa (or not yours)'),
            ('see_fa_list', 'See list of fa itself'),

            ('add_fa', 'Create an fa'),

            ('change_fa', 'Obrigatory for user can change any fa'),
            ('change_own_fa', 'Change own fa (or itself)'),
            ('change_other_fa', 'See other fa (or not yours)'),

            ('delete_fa', 'Obrigatory for user can change any fa'),
            ('delete_other_fa', 'Delete other fa (or not yours)'),
        )

    clients = models.ManyToManyField(
        ActiveClient,
        related_name='financial_advisers'
    )

    # To facilitate getting default permissions in others places
    @property
    def default_permissions(self):
        permissions_codenames = [
            'see_client', 'delete_client', 'change_client',
            'see_own_client', 'delete_own_client', 'change_own_client'
            'see_other_client', 'add_client'

            'see_employee', 'delete_employee', 'change_employee',
            'see_other_employee', 'delete_other_employee', 'add_employee'

            'see_fa', 'delete_fa', 'change_fa',
            'see_own_fa', 'delete_own_fa', 'change_own_fa'
            'see_other_fa', 'delete_other_fa', 'add_fa'
        ]

        permissions = []
        for permission_codename in permissions_codenames:
            permissions += \
                [Permission.objects.get(codename=permission_codename)]

        return permissions
