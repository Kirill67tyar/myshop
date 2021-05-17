from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (CharField,
                              DateTimeField,
                              IntegerField,
                              BooleanField,
                              Model, )


class Coupon(Model):
    code = CharField(max_length=50, unique=True, verbose_name='Код купона')
    valid_from = DateTimeField(verbose_name='Начало действия купона')
    valid_to = DateTimeField(verbose_name='Конец действия купона')
    discount = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100), ],
                            verbose_name='Скидка')
    active = BooleanField(verbose_name='Активен')

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

# благодаря валидаторам MinValueValidator(0) и MaxValueValidator(100)
# мы не можем ввести значение <0 и >100. Наш discount может быть строго 0<=discount<=100
# Обрати внимание что это модель а не форма, а аргумент validators есть