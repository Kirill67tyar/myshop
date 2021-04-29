from django.forms import ModelForm
from orders.models import Order


class CreateOrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'city',
            'address',
            'postal_code',
        ]
