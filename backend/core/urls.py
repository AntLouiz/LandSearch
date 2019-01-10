from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.upload_file, name='index'),
]
