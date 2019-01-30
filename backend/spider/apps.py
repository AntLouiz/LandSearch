from django.apps import AppConfig
from settings.base import BASE_DIR


class DefaultApp(AppConfig):
    label = 'spider'
    name = 'backend.spider'
    path = BASE_DIR.child('backend', 'spider')
    verbose_name = 'Spider Application'
