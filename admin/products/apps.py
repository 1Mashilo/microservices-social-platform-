from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuration class for the 'products' Django application.

    Attributes:
        name (str): The name of the application ('products').
    """
    name = 'products'

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'