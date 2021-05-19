from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from shop.models import Product
from coupons.models import Coupon


class Order(models.Model):
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    paid = models.BooleanField(default=False, verbose_name='Оплачен?')
    braintree_id = models.CharField(max_length=200, blank=True, verbose_name='ID чека')
    coupon = models.ForeignKey('coupons.Coupon',
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='orders',
                               verbose_name='Купон')
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100), ])

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order: {self.pk} | Date: {self.created} | To: {self.email}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE,
                              related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='order_items', verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.pk)

    def get_cost(self):
        return self.price * self.quantity
