from django.apps import AppConfig


class StoreTopzeraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_topzera'

    def ready(self):
        import store_topzera.signals   
        from django.contrib.auth.models import User
        from store_topzera.models import Cliente

        def cliente(self):
            try:
                return Cliente.objects.get(user=self)
            except Cliente.DoesNotExist:
                return None

        User.add_to_class('cliente', property(cliente)) 