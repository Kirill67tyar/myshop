# import weasyprint

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings

from orders.forms import CreateOrderModelForm
from orders.models import OrderItem, Order
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


# staff_member_required - проверяет у request.user - is_staff==True и admin==True
@staff_member_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    template_name = 'admin/orders/order/detail.html'
    return render(request, template_name=template_name, context={'order': order, })


@staff_member_required
def order_in_pdf_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    template_html = render_to_string(template_name='orders/pdf.html',
                                     context={'order': order})
    response = HttpResponse(content_type='application/pdf')
    # для pdf здесь почему-то в знаечнии заголовка не надо прикреплять 'attachment;'
    response['Content-Disposition'] = f'filename=order_{order.pk}.pdf'
    # weasyprint.HTML(string=template_html).write_pdf(response,
    #                                                 stylesheets=[weasyprint.CSS(
    #                                                     settings.STATIC_ROOT + 'css/pdf.css')])
    return response
