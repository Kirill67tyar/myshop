# import weasyprint - не работает
from fpdf import FPDF, HTMLMixin

from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, reverse, redirect, get_object_or_404

from cart.cart import Cart
from orders.models import OrderItem, Order
from orders.tasks import order_created_task
from orders.forms import CreateOrderModelForm

"""
Libraries:

fpdf - https://pyfpdf.readthedocs.io/en/latest/index.html
fpdf - https://pypi.org/project/fpdf/
fpdf - https://python-scripts.com/create-pdf-pyfpdf
"""


class WriteHTMLinPDF(FPDF, HTMLMixin):
    pass


def create_order_view(request):
    cart = Cart(request=request)
    if request.method == 'POST':
        form = CreateOrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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
# и если да, то дает дальнейший доступ к функции (а если нет, то скорее всего status_code - Forbidden)
@staff_member_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    template_name = 'admin/orders/order/detail.html'
    return render(request, template_name=template_name, context={'order': order, })


@staff_member_required
def order_detail_in_pdf_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    template_html = render_to_string(template_name='orders/pdf.html',
                                     context={'order': order})

    pdf = WriteHTMLinPDF()
    pdf.add_page()
    pdf.write_html(template_html)
    content = pdf.output(f'order_{order.pk}.pdf', 'S').encode('latin-1')

    # HttpResponse - working version
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.pk}.pdf'
    response.write(content=content)

    # FileResponse
    response1 = FileResponse(content, content_type='application/pdf', filename=f'filename=order_{order.pk}.pdf')
    response1['Content-Disposition'] = f'filename=order_{order.pk}.pdf'
    return response
