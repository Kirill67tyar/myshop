from django.template.loader import render_to_string
from django.test import TestCase
from orders.models import Order

order = Order.objects.first()

template_html = render_to_string(template_name='orders/pdf.html',
                                     context={'order': order})
