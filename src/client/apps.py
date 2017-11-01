from django.apps import AppConfig


class ClientConfig(AppConfig):
    name = 'client'

    def ready(self):
        try:
            import client.signals  # pylint: disable=unused-variable
        except ImportError:
            raise ImportError(
                "Couldn't import client.signals. This file must exists."
            )
