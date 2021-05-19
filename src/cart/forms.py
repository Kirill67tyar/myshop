from django import forms
from django.utils.translation import gettext_lazy as _

class CartAddProductForm(forms.Form):

    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_('Quantity'))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

# TypedChoiceField с параметром coerce=int позволяет автоматически преобразовать выбранное значение
# в целое число (точнее в тот тип данных, что указан в аргументе coerce=)
# HiddenInput - чтобы пользователь не видел это поле в своей форме.
# initial - это дефолтное значение этого поля как default в модели
# но initial, который мы передаем как именованный аргумент непосредственно в форму -
# означает какие значения по умоланию для аттрибутов вызвать в форме
# смотри - отличный пример как выполняется аргумент initial в контроллере cart/views.py - detail_cart_view