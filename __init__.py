from settings.celery_settings import app as celery_app
print(celery_app)
__all__ = ['celery_app']
