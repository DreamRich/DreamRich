from django.db.models.signals import post_save
from django.dispatch import receiver
from client.models import ActiveClient
from rolepermissions.roles import assign_role


@receiver(post_save, sender=ActiveClient)
def permission_financial_adviser(sender,  # pylint: disable=unused-argument
                                 instance,
                                 **unused_kwargs):
    assign_role(instance, 'client')
