from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product
from shop.utils import get_view_at_console, get_view_at_console2

from cart.forms import CartAddProductForm


def experiments(request):
    """
    obj, delimiter='*', unpack=False, sep='\n'
    """
    # get_view_at_console(request.session.keys(), unpack=0, delimiter='+')
    # get_view_at_console(request.session.values(), unpack=0, delimiter='=')
    # get_view_at_console(request.session.items(), unpack=0, delimiter='*')
    # get_view_at_console(request.session.get('_auth_user_hash'), unpack=0, delimiter='^')
    # get_view_at_console(request.session, unpack=0, delimiter='#')
    # get_view_at_console(request, unpack=1, delimiter='#')
    # request.session['foo'] = 'bar'
    # get_view_at_console(request.session['foo'], unpack=0, delimiter='#')
    # del request.session['foo']
    # try:
    #     get_view_at_console(request.session['foo'], unpack=0, delimiter='#')
    # except KeyError:
    #     print('Key "foo" and value "bar" does not exists anymore', end='\n\n\n')
    # try:
    #     print(request.__name__)
    # except AttributeError:
    #     print('request has not attribute __name__', end='\n\n\n')
    # get_view_at_console(Product)
    # get_view_at_console(request.session.modified)
    # get_view_at_console(request, unpack=True)
    # get_view_at_console(settings.SESSION_ENGINE)
    # email_sent = send_mail('some subject', 'mail came', settings.EMAIL_HOST_USER, ['kirillbogomolov.ric@yandex.ru'])
    # return email_sent
    return 'experiment'


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
        'add_quantity_product_to_cart_form': CartAddProductForm,
    }
    return render(request, 'shop/product/detail.html', context=context)



