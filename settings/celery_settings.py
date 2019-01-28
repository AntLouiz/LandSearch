import os
from celery import Celery
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery('backend')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()