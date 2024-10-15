from django.apps import AppConfig


class LoyaltyModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loyalty_models'

    def ready(self):
        from .signals import (
            check_tier_change
        )
