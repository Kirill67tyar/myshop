from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product
from shop.utils import get_view_at_console, get_view_at_console2


def experiments(request):
    # get_view_at_console(request.session.keys(), unpack=0, delimiter='+')
    # get_view_at_console(request.session.values(), unpack=0, delimiter='=')
    # get_view_at_console(request.session.items(), unpack=0, delimiter='*')
    # get_view_at_console(request.session.get('_auth_user_hash'), unpack=0, delimiter='^')
    # get_view_at_console(request.session, unpack=0, delimiter='#')
    request.session['foo'] = 'bar'
    get_view_at_console(request.session['foo'], unpack=0, delimiter='#')
    del request.session['foo']
    try:
        get_view_at_console(request.session['foo'], unpack=0, delimiter='#')
    except KeyError:
        print('Key "foo" and value "bar" more does not exists', end='\n\n\n')


def product_list_view(request, category_slug=None):
    categories = Category.objects.all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
    else:
        products = Product.objects.filter(available=True)
    context = {
        'products': products,
        'categories': categories,
        'category': category,
    }
    return render(request, 'shop/product/list.html', context=context)


def product_detail_view(request, id, slug):
    experiments(request)

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
