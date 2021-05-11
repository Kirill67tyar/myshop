from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug, ])


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория')
    name = models.CharField(max_length=250, db_index=True, verbose_name='Название товара')
    slug = models.SlugField(max_length=250, db_index=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фото товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Есть ли в наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Когда добавлен')
    updated = models.DateTimeField(auto_now=True, verbose_name='Когда обновлён')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug',),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {
            'id': self.id,
            'slug': self.slug,
        }
        return reverse('shop:product_detail', kwargs=kwargs)

# Для таблицы shop_product где внешний ключ category_id - это отношение не Один ко Многим, а 
# Многие к Одному
# Столбик price в db будет иметь тип данных decimal а не integer
