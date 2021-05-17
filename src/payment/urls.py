from django.urls import path
from payment.views import (payment_process_view,
                           payment_canceled_view,
                           payment_done_view,
                           experiment, )

app_name = 'payment'

urlpatterns = [
    path('process/', payment_process_view, name='process'),
    path('done/', payment_done_view, name='done'),
    path('canceled/', payment_canceled_view, name='canceled'),

    path('experiment/', experiment, name='payment_experiment'),
]
