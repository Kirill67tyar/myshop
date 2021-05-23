from parler.admin import TranslatableAdmin

from django.contrib import admin
from shop.models import Category, Product

# ------------------------------------------------------------FOR  TranslatableAdmin
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('pk', 'name', 'slug',)

    # prepopulated_fields = {'slug': ('name',)}# - не работает с TranslatableAdmin
    def get_prepopulated_fields(self, request, obj=None):  # вместо prepopulated_fields
        return {'slug': ('name',), }


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    # list_display - то что мы видим в общем списке
    list_display = ('pk', 'name', 'slug', 'price', 'available', 'created', 'updated')
    # list_filter - те поля, по которым мы можем фильтровать
    list_filter = ('available', 'created', 'updated', )
    # list_editable - добавляет возможность изменять перечисленные поля со страницы списков
    # но все поля list_editable должны быть обязательно в list_display
    list_editable = ('price', 'available', )

    # prepopulated_fields = {'slug': ('name',),}# - не работает с TranslatableAdmin
    def get_prepopulated_fields(self, request, obj=None):  # вместо prepopulated_fields
        return {'slug': ('name',), }




# ------------------------------------------------------------FOR  ModelAdmin
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name', 'slug',)
#
#     # prepopulated_fields = {'slug': ('name',)}# - не работает с TranslatableAdmin
#     # def get_prepopulated_fields(self, request, obj=None):  # вместо prepopulated_fields
#     #     return {'slug': ('name',), }
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # list_display - то что мы видим в общем списке
#     list_display = ['pk', 'name', 'slug', 'price', 'available', 'created', 'updated']
#     # list_filter - те поля, по которым мы можем фильтровать
#     list_filter = ['available', 'created', 'updated', ]
#     # list_editable - добавляет возможность изменять перечисленные поля со страницы списков
#     # но все поля list_editable должны быть обязательно в list_display
#     list_editable = ['price', 'available', ]
#
#     # prepopulated_fields = {'slug': ('name',),}# - не работает с TranslatableAdmin
#     # def get_prepopulated_fields(self, request, obj=None):  # вместо prepopulated_fields
#     #     return {'slug': ('name',), }




