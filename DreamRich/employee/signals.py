from django.db.models.signals import post_save
from employee.models import FinancialAdviser, Employee
from django.dispatch import receiver
from rolepermissions.roles import assign_role

@receiver(post_save,sender=FinancialAdviser)
def permission_financial_adviser(sender, instance, **kwargs):
    assign_role(instance, 'financial_adviser')

@receiver(post_save,sender=Employee)
def permission_employee(sender, instance, **kwargs):
    assign_role(instance, 'comum_employee')
