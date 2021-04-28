from django.urls import path
from cart.views import add_cart_view, remove_cart_view, detail_cart_view

app_name = 'cart'

urlpatterns = [
    path('', detail_cart_view, name='detail_cart'),
    path('add/<int:product_id>/', add_cart_view, name='add_cart'),
    path('remove/<int:product_id>/', remove_cart_view, name='remove_cart'),
]
