from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm


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


# update_quantity_form
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
    return render(request, 'cart/detail.html', {'cart': cart, })
