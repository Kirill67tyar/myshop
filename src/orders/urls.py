from django.urls import path
from orders.views import create_order_view

app_name = 'orders'

urlpatterns = [
    path('create/', create_order_view, name='create_order'),
]
