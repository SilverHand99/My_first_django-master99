from django.apps import AppConfig


class MyProjektConfig(AppConfig):
    name = 'my_projekt'

    def ready(self):
        import my_projekt.signals
