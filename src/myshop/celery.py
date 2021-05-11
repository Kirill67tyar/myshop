import os
from celery import Celery

"""
Импортируем celery и os и выполняем 5 шага
"""

# 1) задаем переменную окружения, содержащую название файла настроек нашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# 2) создаем экземпляр класса Celery
app = Celery('myshop')

# 3) загружаем конфигурацию настроек из нашего проекта вызывая метод config_from_object
# аргумент namespace - определяет префикс, который мы будем определять для всех настроек
# связанных с Celery
# Вспомни, что settings мы импортирум - from django.conf import settings
# таким образом в settings.py можно будет задавать конфигурацию Celery добавляя
# в начало CELERY_ например CELERY_BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4) запускаем процесс поиска и загрузки асинхронный задач по нашему проекту
# celery пройдет по всем приложеняим INSTALLED_APPS в поисках файла tasks.py
# чтобы загрузить код задач.
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# 5) шаг - в __init__.py проекта добавит строчку:
# from myshop.celery import app as celery_app
# Таким образом он будет выполняться при старте проекта