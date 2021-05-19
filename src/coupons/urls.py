from django.urls import path

from coupons.views import coupon_apply_view, coupon_delete_view

app_name = 'coupons'

urlpatterns = [
    path('apply/', coupon_apply_view, name='apply'),
    path('delete/', coupon_delete_view, name='delete'),
]
