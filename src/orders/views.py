from django.shortcuts import render, reverse, redirect

from orders.forms import CreateOrderModelForm
from orders.models import OrderItem
from orders.tasks import order_created_task
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
            # метод delay() - запускает задачу асинхронно
            # order_created_task.delay(order.pk)
            order_created_task(order.pk)
            request.session['order_id'] = order.pk
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/create_done.html', {'order': order, })
    else:
        form = CreateOrderModelForm()
    return render(request, 'orders/create.html', {'form': form, })
