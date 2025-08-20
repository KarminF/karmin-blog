from django.apps import AppConfig
from django.db.utils import OperationalError
from django.contrib.auth import get_user_model


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        try:
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="admin123"
                )
        except OperationalError:
            pass