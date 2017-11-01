from django.db.models.signals import post_save
from django.dispatch import receiver
from employee.models import FinancialAdviser, Employee
from rolepermissions.roles import assign_role


@receiver(post_save, sender=FinancialAdviser)
def permission_financial_adviser(sender,  # pylint: disable=unused-argument
                                 instance,
                                 **unused_kwargs):
    assign_role(instance, 'financial_adviser')


@receiver(post_save, sender=Employee)
def permission_employee(sender,  # pylint: disable=unused-argument
                        instance,
                        **unused_kwargs):
    assign_role(instance, 'employee')
