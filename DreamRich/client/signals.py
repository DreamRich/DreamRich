from django.db.models.signals import post_save
from client.models import ActiveClient
from django.dispatch import receiver
from rolepermissions.roles import assign_role

@receiver(post_save,sender=ActiveClient)
def permission_financial_adviser(sender, instance, **kwargs):
    assign_role(instance, 'client')
