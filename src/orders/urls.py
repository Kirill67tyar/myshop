from django.urls import path
from orders.views import create_order_view, order_detail_view, order_detail_in_pdf_view

app_name = 'orders'

urlpatterns = [
    path('create/', create_order_view, name='create_order'),
    path('order_detail/<int:order_id>/', order_detail_view, name='order_detail'),
    path('order_pdf/<int:order_id>/', order_detail_in_pdf_view, name='order_detail_in_pdf'),
]
