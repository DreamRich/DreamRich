from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmployeeConfig(AppConfig):
    name = 'employee'

    def ready(self):
        import employee.signals
