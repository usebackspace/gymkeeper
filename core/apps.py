from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

from django.db.models.signals import post_migrate
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'core'

    def ready(self):
        from .signals import create_subscription_plans
        post_migrate.connect(create_subscription_plans, sender=self)
