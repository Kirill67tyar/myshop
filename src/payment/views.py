import braintree
from io import BytesIO
from fpdf import FPDF, HTMLMixin

from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import (render, redirect, reverse, get_object_or_404, )

from orders.models import Order
from orders.views import WriteHTMLinPDF
from shop.utils import get_view_at_console1

"""
<QueryDict: {'payment_method_nonce': ['tokencc_bh_p24xj7_h2mpmy_hvvxpy_8bfjmf_wn6'], 
'csrfmiddlewaretoken': ['vdTCYKQ8Xur0wat9Bkb8C6vnMCYofO9VhYs4FsuE7Hus6m3uxgdeMCfvWgFur7gH']}>

Так выглядит QueryDict при post запросе. Никаких cvv, card-number, expiration-date
"""


def experiment(request):
    order = Order.objects.first()
    send_order_by_email_in_pdf(order)
    return JsonResponse({'status': 'ok', })


def send_order_by_email_in_pdf(order):
    subject = f'My Shop. Счет по заказу {order.pk}'
    message = f'Ваш счет по заказу {order.pk} в формате PDF. Вы можете его скачать'
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email, ])
    template_html = render_to_string('payment/pdf.html',
                                     context={'order': order, })
    pdf = WriteHTMLinPDF()
    pdf.add_page()
    pdf.write_html(template_html)
    content = pdf.output(f'order_{order.pk}.pdf', 'S').encode('latin-1')

    email.attach(filename=f'order_{order.pk}.pdf', content=content, mimetype='application/pdf')
    return email.send()


def payment_process_view(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':

        get_view_at_console1(request.POST)

        # достаем из тела запроса защищенный токен транзакции,
        # который делает JS SDK от Braintree
        # зная токен из обработчика (client_token) javascript SDK Braintree
        # сформирует защищенную форму
        # и при заполенении этой формы и отпраке post запроса
        # js sdk уже сформирует защищенный токен транзакции
        nonce = request.POST.get('payment_method_nonce', None)

        # создание и отпрака транзакции (идентификатор платежной транзакции)
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),  # - общая сумма заказа
            'payment_method_nonce': nonce,  # - token для платежной транзакции
            'options': {
                'submit_for_settlement': True,  # options - Дополнительные параметры
            },  # submit_for_settlement = True - транзакция будет обрабатываться автоматически
        })

        if result.is_success:
            order.paid = True
            # сохраняем уникальный id транзакции
            order.braintree_id = result.transaction.id
            order.save()
            send_order_by_email_in_pdf(order)
            return redirect(reverse('payment:done'))
        else:
            return redirect(reverse('payment:canceled'))
    else:
        # при get запросе
        # генерация одноразового токена для передачи в шаблон и
        # последубщего использования в javascript SDK Braintree
        client_token = braintree.ClientToken.generate()
        context = {
            'order': order,
            'client_token': client_token,
        }
        return render(request, 'payment/process.html', context=context)


def payment_done_view(request):
    return render(request, 'payment/done.html', {})


def payment_canceled_view(request):
    return render(request, 'payment/canceled.html', {})
