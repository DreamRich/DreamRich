from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    name = 'employee'

    def ready(self):
        try:
            import employee.signals  # pylint: disable=unused-variable
        except ImportError:
            raise ImportError(
                "Couldn't import client.signals. This file must exists."
            )
