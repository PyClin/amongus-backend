from django.apps import AppConfig


class AmongUsConfig(AppConfig):
    name = 'amongus'

    def ready(self):
        import amongus.signals