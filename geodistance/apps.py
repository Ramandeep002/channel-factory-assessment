"""
App configuration for the geodistance app.

This module configures the geodistance app within the Django project.
"""
from django.apps import AppConfig

class GeodistanceConfig(AppConfig):
    """
    AppConfig for the geodistance app.

    This class configures settings specific to the geodistance app,
    such as the default auto field for models and the app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geodistance'
