from django.apps import AppConfig


class MallConfig(AppConfig):
    name = 'mall'

    def ready(self):
        import mall.signals
