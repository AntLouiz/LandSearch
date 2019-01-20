from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('get_region', views.upload_file, name='new_order'),
    path('orders', views.OrdersListView.as_view(), name='orders'),
    path('order/<int:pk>', views.OrderDeleteView.as_view(), name='delete_order')
]
