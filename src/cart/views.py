from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm




@require_POST
def add_cart_view(request, product_id):
    pass

def remove_cart_view(request, product_id):
    pass

def detail_cart_view(request):
    pass