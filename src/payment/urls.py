from django.urls import path
from django.utils.translation import gettext_lazy as _

from payment.views import (payment_process_view,
                           payment_canceled_view,
                           payment_done_view,
                           experiment, )

app_name = 'payment'

urlpatterns = [
    path(_('process/'), payment_process_view, name='process'),
    path(_('done/'), payment_done_view, name='done'),
    path(_('canceled/'), payment_canceled_view, name='canceled'),

    path('experiment/', experiment, name='payment_experiment'),
]
