from django.contrib import admin
from shop.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display - то что мы видим в общем списке
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    # list_filter - те поля, по которым мы можем фильтровать
    list_filter = ['available', 'created', 'updated',]
    # list_editable - добавляет возможность изменять перечисленные поля со страницы списков
    # но все поля list_editable должны быть обязательно в list_display
    list_editable = ['price', 'available',]
    prepopulated_fields = {'slug': ('name',),}
