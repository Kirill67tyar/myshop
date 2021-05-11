from django.core.mail import send_mail
from django.conf import settings

from celery import Task#, task

from orders.models import Order


# @task
def order_created_task(order_id):
    order = None
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        pass
    if order:
        subject = f'Заказ № {order.pk}'
        message = f'Ваш заказ успешно оформлен. Номер заказа - {order.pk}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [order.email, ]
        named_args = {
            'subject': subject,
            'message': message,
            'from_email': from_email,
            'recipient_list': recipient_list,
        }
        email_sent = send_mail(**named_args)
        return email_sent

# Короче Celery - не работает, потому что декоратор task  устарел:
# https://stackoverflow.com/questions/64483648/django-and-celery-modulenotfounderror-no-module-named-celery-task
# https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html?highlight=periodic
