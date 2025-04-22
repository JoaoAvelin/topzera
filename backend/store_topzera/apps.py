from django.apps import AppConfig


class StoreTopzeraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_topzera'

    def ready(self):
        import store_topzera.signals    