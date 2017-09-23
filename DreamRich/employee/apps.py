from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    name = 'employee'

    def ready(self):
        import employee.signals
        employee.signals
