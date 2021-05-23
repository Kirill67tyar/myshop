"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'coupons.apps.CouponsConfig',
    'rosetta',
    'parler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# список всех кодов языка:
# http://www.i18nguy.com/unicode/language-identifiers.html
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en'  # 'ru-ru'#'en-us'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'UTC'

USE_I18N = True  # включена ли интернационализация

USE_L10N = True  # включена ли локализация для дат, времени и чисел

USE_TZ = True  # использовать ли даты с учетом временной зоны

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# -------------------------------------------------------- STATIC settings

STATIC_URL = '/static/'

# здесь мы указываем откуда будем доставать статику и подключать к шаблону,
# с помощью тега {% static 'css/style.css' %}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# здесь мы указываем куда django будет собирать всю статику проекта при команде collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
# -------------------------------------------------------- STATIC settings


# -------------------------------------------------------- MEDIA settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# -------------------------------------------------------- MEDIA settings


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ключ для сессии, конкретно для корзины покупок
CART_SESSION_ID = 'cart'

# # email backend, который позвляет нам вместо почты (работы с SMTP сервером) использовать консоль
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# -------------------------------------------------------- SMTP-server settings
# # email backend, который позвляет нам вместо почты (работы с SMTP сервером) использовать консоль
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#                   ^----^----^ OR v----v----v
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
# -------------------------------------------------------- SMTP-server settings


# -------------------------------------------------------- BRAINTREE settings
# docs:
# https://github.com/Kirill67tyar/braintree_python
# https://developers.braintreepayments.com/start/hello-server/python
import braintree

BRAINTREE_MERCHANT_ID = os.getenv('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = os.getenv('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = os.getenv('BRAINTREE_PRIVATE_KEY')

#                     v----v----v

# gateway = braintree.BraintreeGateway(
#     braintree.Configuration(
#         braintree.Environment.Sandbox,
#         merchant_id=BRAINTREE_MERCHANT_ID,
#         public_key=BRAINTREE_PUBLIC_KEY,
#         private_key=BRAINTREE_PRIVATE_KEY
#     )
# )
# #                   ^----^----^ OR v----v----v
braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    # Environment.Production,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)
#                                   ^----^----^
# Важно! - для боевого режима нужен аккаунт полноценный https://www.braintreegateway.com/
# Merchant ID, Public key и Private key там нужно получать другие
# и заменить их соответсвенно

# И вместо braintree.Environment.Sandbox нужно использовать braintree.Environment.Production

# Sandbox - для тренировки, или отладке, проверке что все рабтает
# Production - для продакшн) Для боевого режима

# если интересует версия для локального сервера (не продакшн), то:
# https://sandbox.braintreegateway.com/merchants/nv5dfpjh7jv353hc/home

# для пробного варианта используй карту:
# № 4111 1111 1111 1111
# CVV - 123
# date - 12/24
# -------------------------------------------------------- BRAINTREE settings


# -------------------------------------------------------- DJANGO-PARLER settings

PARLER_LANGUAGES = {
    None: (
        {'code': 'en', },
        {'code': 'ru', },
    ),
    'default': {
        'fallbacks': 'en',  # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,  # the default; let .active_translations() return fallbacks too. (прятать или нет)
    }
}
# -------------------------------------------------------- DJANGO-PARLER settings
