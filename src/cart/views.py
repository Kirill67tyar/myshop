from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, reverse, get_object_or_404

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.models import Product
from shop.recommender import Recommender
from coupons.forms import CouponApplyForm


@require_POST
def add_cart_view(request, product_id):
    cart = Cart(request=request)
    product = get_object_or_404(Product, pk=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        kwargs = {
            'product': product,
            'quantity': cd['quantity'],
            'update_quantity': cd['update'],
        }
        cart.add(**kwargs)
    return redirect(reverse('cart:detail_cart'))


def remove_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product=product)
    return redirect(reverse('cart:detail_cart'))


def detail_cart_view(request):
    cart = Cart(request)
    # Здесь мы приваиваем нашему итерируемому объекту корзины
    # еще форму, с уже проинициализированными аттрибутами.
    # К этому аттрибуту-форме мы будем обращаться в шаблоне
    # для посылки post запроса через тег <form ...> к обработику add_cart_view
    for item in cart:
        initial = {
            'quantity': item['quantity'],
            'update': True,
        }
        item['update_quantity_form'] = CartAddProductForm(initial=initial)

    r = Recommender()
    products = [item['product'] for item in cart]
    recommended_products = None
    if products:
        recommended_products = r.suggest_products_for(products=products, max_results=4)
    context = {
        'cart': cart,
        'coupon_apply_form': CouponApplyForm,
        'recommended_products': recommended_products,
    }
    return render(request, 'cart/detail.html', context=context)
