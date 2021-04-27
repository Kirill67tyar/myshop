from django import forms


class CartAddProductForm(forms.Form):

    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

# TypedChoiceField с параметром coerce=int позволяет автоматически выбранное значение
# в целое число (или тот тип данных, что указан в аргументе coerce=)
# HiddenInput - чтобы пользователь не видел это поле в своей форме.