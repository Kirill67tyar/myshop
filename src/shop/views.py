from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product


def product_list_view(request, category_slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'products': products,
        'categories': categories,
        'category': category,
    }
    return render(request, 'shop/product/list.html', context=context)


def product_detail_view(request, id, slug):
    kwargs = {
        'klass': Product,
        'id': id,
        'slug': slug,
        'available': True,
    }
    product = get_object_or_404(**kwargs)
    context = {
        'product': product,
    }
    return render(request, 'shop/product/detail.html', context=context)


