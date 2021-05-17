"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# myshop_admin

# ---------------------------------------------------------------------- braintree
# панель для системы оплаты braintree - demo version (не для продакшн).
# https://sandbox.braintreegateway.com/merchants/nv5dfpjh7jv353hc/home
# именно от сюда берется BRAINTREE_MERCHANT_ID, BRAINTREE_PUBLIC_KEY и BRAINTREE_PRIVATE_KEY

# для пробного варианта используй карту:
# № 4111 1111 1111 1111
# CVV - 123
# date - 12/24
# ---------------------------------------------------------------------- braintree


# ---------------------------------------------------------------------- weasyprint
# Документация для weasyprint:
# https://weasyprint.readthedocs.io/en/stable/
# https://pypi.org/project/weasyprint/

# Сам weasyprint:
# https://weasyprint.org/

# Установлен MSYS2 - C:\msys32

# Проблемы при обновлении ключей
# https://blog.altuninvv.ru/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/35-%D0%BA%D0%B0%D0%BA-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%B8%D1%82%D1%8C-msys2-%D0%BF%D1%80%D0%B8-%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D0%B5-%D0%BD%D0%B5%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%BD%D1%8B%D0%B9-%D0%BA%D0%BB%D1%8E%D1%87

# Очень важно, при работе с weasyprint нужно добавить переменную окружения:
# PATH - C:\msys32\mingw32\bin

# pacman -Syu

# Короче, этот weasyprint слишком дохуя требует, изменения переменной окружения PATH
# и т.д. Плюс гемора с ним очень много. Нахуй его(её), этот weasyprint.
# А в результате кстати все равно нихуя не работает,
# библиотека нормально импортироваться не может)



# Так что будем работать с FPDF
#
# https://python-scripts.com/create-pdf-pyfpdf
# https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
# https://pypi.org/project/fpdf/
# ---------------------------------------------------------------------- weasyprint



