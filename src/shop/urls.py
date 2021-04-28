from django.urls import path
from shop.views import product_list_view, product_detail_view

app_name = 'shop'

urlpatterns = [
    path('', product_list_view, name='product_list'),
    path('<slug:category_slug>/', product_list_view, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', product_detail_view, name='product_detail'),

]
