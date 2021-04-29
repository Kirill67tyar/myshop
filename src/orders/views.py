from django.shortcuts import render

from orders.forms import CreateOrderModelForm
from orders.models import OrderItem
from cart.cart import Cart


def create_order_view(request):
    cart = Cart(request=request)
    if request.method == 'POST':
        form = CreateOrderModelForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                kwargs = {
                    'order': order,
                    'product': item['product'],
                    'price': item['price'],
                    'quantity': item['quantity'],
                }
                OrderItem.objects.create(**kwargs)
            cart.clear()
            return render(request, 'orders/create_done.html', {'order': order, })
    else:
        form = CreateOrderModelForm()
    return render(request, 'orders/create.html', {'form': form, })
