import datetime
import csv

from django.http import HttpResponse
from django.contrib import admin

from orders.models import Order, OrderItem
from shop.utils import get_view_at_console1


# ------------------------------------------------------------------------ export to csv
def export_to_csv(modeladmin, request, queryset):
    """
    Функция, позволяющая скаать csv файл заказов.
    Эта функция выполняется когда пользователь выберет действие на сайте администрирования
    Создавалась первонаально для Order но подходит и для других моделей.
    Просто добавьте аттрибут actions в классу заимствованному от ModelAdmin:

    actions = [export_to_csv, ]

    Принимает три аргумента:
    -- объект ModelAdmin, которая будет отображаться
    -- объект request - экземпляр класса HttpRequest
    -- QuerySet объектов, которые выбрал пользователь
    """

    # 1) получаем экземпляр Options связанный с работающей моделью (в данном случае Order)
    opts = modeladmin.model._meta

    # 2) Начинаем формировать наш response с заголовком content_type='text/csv'
    # благодаря этому заголовку браузер будет работать с файлом также как и с csv
    response = HttpResponse(content_type='text/csv')

    # 3) добавляем заголовок Content-Disposition
    # Content-Disposition -- прикрепляет к ответу файл
    response['Content-Disposition'] = f'attachment;filename={opts.verbose_name}.csv'

    # 4) создаем объект writer, который будет записывать данные в файл - объект response
    writer = csv.writer(response)

    # 5) получаем поля нашей модели за исключением many_to_many и one_to_many
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # 6) заполняем строку заголовок названиями полей
    writer.writerow([field.verbose_name for field in fields])

    # 7) проходим по нашему queryset и если и от каждого экземпляра модели
    # получаем данные ее полей. Если поле экземпляр datetime то приобразовываем к формату str
    # дальше записываем строку в экземпляр writer
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    # get_view_at_console1(response.content, unpack=0)

    # возвращаем наш response
    return response


# 8) добавляем как действие будет отображаться на сайте администрирования
export_to_csv.short_description = 'Export to CSV'


# ------------------------------------------------------------------------ export to csv


class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product', ]


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name',
                    'email', 'address', 'postal_code',
                    'city', 'created', 'updated', 'paid', ]

    list_filter = ['paid', 'created', 'updated', ]
    inlines = [OrderItemTabularInline, ]
    actions = [export_to_csv, ]
