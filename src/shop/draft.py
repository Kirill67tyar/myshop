# SEO (search engine optimization) - поисковая оптимизация. Гугли это.

# В urlpatterns хрянтся шаблоны обработчика
# Во всяком случае функция path(...) - называется шаблон для обработчика
# Или шаблон для URL'a

# логика добавления шаблонов url (как правило) - от более частных к более общим
# (общие могут просто перекрыть частные)

#                   Сессия (Sessions)
#
"""
sourses:
https://developer.mozilla.org/ru/docs/Web/HTTP/Session
https://ru.wikipedia.org/wiki/%D0%A1%D0%B5%D1%81%D1%81%D0%B8%D1%8F_(%D0%B2%D0%B5%D0%B1-%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0)
https://codenamecrud.ru/ruby-on-rails/sessions-cookies-and-authentication

from django.contrib.sessions.middleware import SessionMiddleware

HTTP сессия
Так как HTTP — это клиент-серверный протокол, HTTP сессия состоит из трёх фаз:

Клиент устанавливает TCP соединения (или другое соединение, если не используется TCP транспорт).
Клиент отправляет запрос и ждёт ответа.
Сервер обрабатывает запрос и посылает ответ, в котором содержится код статуса и соответствующие данные.
Начиная с версии HTTP/1.1, после третьей фазы соединение не закрывается,
так как клиенту позволяется инициировать другой запрос. То есть, вторая и третья фазы могут повторяться.

Понятие "Сессий" основано на том, что состояние пользователя каким-то образом сохраняется,
когда он переходит с одной страницы на другую. Вспомните, что HTTP не сохраняет состояний,
поэтому только браузер или ваше приложение может "запомнить" то, что нужно запомнить.



                                    Django сессии
Все взаимодействия между браузерами и серверами осуществляются при помощи протокола HTTP,
который не сохраняет своё состояние (stateless). Данный факт означает, что сообщения между клиентом
и сервером являются полностью независимыми один от другого — то есть не существует какого-либо
представления "последовательности", или поведения в зависимости от предыдущих сообщений.
В результате, если вы хотите создать сайт который будет отслеживать взаимодействие с клиентом (браузером),
вам нужно реализовать это самостоятельно.

Сессии являются механизмом, который использует Django (да и весь остальной "Интернет")
для отслеживания "состояния" между сайтом и каким-либо браузером. Сессии позволяют вам хранить
произвольные данные браузера и получать их в тот момент, когда между данным браузером и сайтом
устанавливается соединение. Данные получаются и сохраняются в сессии при помощи соответствующего "ключа".
(Вспоминай сессионный ключ, который формируется функцией login(request, user)
В данном случае сессионный ключ формируется на стороне сервера, но хранится
я так понимаю на стороне браузера)

Django использует куки (cookie), которые содержат специальный идентификатор сессии,
который выделяет среди остальных, каждый браузер и соответствующую сессию. Реальные данные сессии,
по умолчанию, хранятся в базе данных сайта (это более безопасно, чем сохранять данные в куки, где
они могут быть уязвимы для злоумышленников). Однако, у вас есть возможность настроить Django так,
чтобы сохранять данные сессий в других местах (кеше, файлах, "безопасных" куки). Но всё же хранение
по умолчанию (в бд) является хорошей и безопасной возможностью.
В базе данных django есть таблица django_session где три столбца:
1) session_key
2) session_data
3) expire_date (истекает дата)
Именно в них сохраняется сессионный ключ

На стороне браузера сессионная инфа сохраняется в куках

В django за обработку и установку куков для каждого запроса отвечает
промежутоный слой скорее всего в MIDDLEWARE - django.contrib.sessions.middleware.SessionMiddleware
это проежуточный слой для управления сессиями
каждый HTTP request и response проходит через middleware

Благодаря middleware на доступны сессии в экземпляре запроса request - request.session

request.session.keys():
dict_keys(['_auth_user_id', '_auth_user_backend', '_auth_user_hash'])

request.session.values():
dict_values(['1', 'django.contrib.auth.backends.ModelBackend',
'1e7b45ed1cfb2632e3221aab4b00d5b2b1a500215e556786cebb801f19b53e9d'])

request.session.items():
dict_items([('_auth_user_id', '1'), ('_auth_user_backend', 'django.contrib.auth.backends.ModelBackend'),
('_auth_user_hash', '1e7b45ed1cfb2632e3221aab4b00d5b2b1a500215e556786cebb801f19b53e9d')])

request.session.get('_auth_user_hash'):
1e7b45ed1cfb2632e3221aab4b00d5b2b1a500215e556786cebb801f19b53e9d

По умоланию подсистема сессий сохраняет их в бд, но это можно переопределить
если выбрать другой механизм хранения сессий

Работа с сессиями аналогина работе со словарями
Единтвенное клюи и знаения должны быть сериализуемы в JSON

request.session['foo'] = 'bar'
request.session.get('foo') - 'bar'

!!!                                                                     !!!
Когда пользователь авторизуется на сайте, его анонимная сессия теряется,
и создается новая, ассоциированная с конкретным пользователем. Если ты хранишь
в анонимной сессии данные, которые не должны быть утеряна после авторизации,
необходимо копировать их в новую сессию при входе пользователя
!!!                                                                     !!!

Как уже было сказано сессии сохраняются в бд в таблицу django_session

В django же они являются экземплярами класса Session
приложения django.contrib.sessions

!!! Следующие способы хранения данных в сессии:
-- На основе базы данных - инфа сессии хранится в бд (по умолчанию)
-- На основе файлов - данные сохраняются в файловой системе
-- На основе кеша - данные хранятся в бэкэнде кеширования
можно настроить с помощью конфигурации CACHES в settings.py
Сессии на основе кеша - самый быстрый способ
-- На основе кеша и базы данных - инфа записыывается в бд, но для доступа
к ней обращение идет сначала в кеш, и только в том случае, если там этой
информации уже нет, выполняется запрос в базу данных
-- На основе куков - данные сессий сохраняются в куках, отправляемых в браузер
пользователю.



!!!                                                                     !!!
Django использует формат JSON для сериализации данных сессии. Поэтому важно,
чтобы ключи были string
!!!                                                                     !!!

                            Session settings
doc:
https://docs.djangoproject.com/en/3.2/topics/http/sessions/
https://docs.djangoproject.com/en/3.2/topics/http/sessions/#settings
https://docs.djangoproject.com/en/3.2/ref/settings/

SESSION_COOKIE_AGE - время жизни сессии на основе куков. измеряется в секундах
(по умолчанию 1209600 - 2 недели)

SESSION_COOKIE_DOMAIN - домен для сессий на основе куков. Установить константу
равной домену сайта, или None, чтобы избежать угрозы подмены куков

SESSION_COOKIE_HTTPONLY - булево значение, говорящее о том, может ли сессия на
основе куков быть задана через HTTP и HTTPS или только HTTPS

SESSION_EXPIRE_AT_BROWSER_CLOSE - время жизни сессии на основе куков после
закрытия браузера (проще - время жизни сессии в браузере) по умоланию False
Если установить True - сессия будет заканчиваться при закрытии пользователем браузера

SESSION_SAVE_EVERY_REQUEST - булево значение. Если оно равно True, сессия будет
сохраняться в бд при каждом запросе. При этом время оконания ее действия булет
автоматиески обновляться

!!! Самая важная настройка сессии - SESSION_ENGINE - позволяет указать каким образом
хранить данные сессии (по умолчанию сохраняются в бд, таблицу django_session)
По умоланию SESSION_ENGINE = 'django.contrib.sessions.backends.db'

метод set_expiry() объекта request.session - тоже может изменить время жизни сессии

методы и аттрибуты request.session:
accessed
clear
clear_expired
create
create_model_instance
cycle_key
decode
delete
delete_test_cookie
encode
exists
flush
get
get_expire_at_browser_close
get_expiry_age
get_expiry_date
get_model_class
get_session_cookie_age
has_key
is_empty
items
key_salt
keys
load
model
modified - аттрибут, отвечает за сохранение изменений request.session,
как инимум в нашем коде (присвоить request.session.modified = True), по умолчанию равен False
pop
save
serializer
session_key
set_expiry - можно установить время жизни сессий (callable)
set_test_cookie
setdefault
test_cookie_worked
update
values





----------------------------------------------------------------------------------------------------------
sources:
https://docs.djangoproject.com/en/3.2/ref/templates/api/#built-in-template-context-processors
https://docs.djangoproject.com/en/3.2/ref/templates/api/

from django.template.context_processors import request

                            Контекстный процессор django

как сделать так, чтобы какая-нибудь переменная была доступна на всех шаблонах проекта?
скажем как request

Для этого и существует контекстный процессор. В настройках в константе TEMPLATES по ключу OPTIONS
список подключенных контекстных процессоров. Они устанавливаются автоматически.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [ ----------- ВОТ ЭТО И ЕСТЬ ПОДКЛЮЧЕННЫЕ КОНТЕКСТНЫЕ ПРОЦЕССОРЫ
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

Контекстный процессор - это функция Python, принимающая объект запроса request (request - это и есть объект)
и возвращающая словарь, который будет добавлен в контекст запроса. Этот ссловарь будет добавляться в контекст
любого шаблона, работаюзего с контекстом типа RequestContext.
К их использованию прибегают, когда нужно получить доступ к какимм-либо объектам или
переменным глобально, во всех шаблонах проекта

Пример контекстного процессора:
def cart(request):
    return {'cart': Cart(request=request)}

или посмотри в файле:
from django.template.context_processors import request

Когда мы создаем проект django-admin startproject some_name в проект уже добавляется несколько
контекстных процессоров:
1) django.template.context_processors.debug - Добавляет булевое знаяение debug и переменную
sql_queries содержащую выполненные для запроса SQL инструкции в контексте шаблона

2) django.template.context_processors.request - добавляет объект запроса request в контекст
(request - экземпляр класса HttpRequest)

3) django.contrib.auth.context_processors.auth - добавляет объект текущего пользователя в
переменную user (можен request.user)

4) django.contrib.messages.context_processors.messages - добавляет переменную messages, содержащую
уведомления сформированные для пользователя подсистемой сообщений Django

Есть еще django.template.context_processors.csrf процессор - обезопашивающий проект от
CSRF-атак. Отключить его никак нельзя (во всяком случае без хака django).

Полный список контекстных прочцессоров
https://docs.djangoproject.com/en/3.2/ref/templates/api/#built-in-template-context-processors

И так:
1) создаешь файл в одном из приложений context_processors.py
2) создаешь там функцию которая будет принимать request и возвращать определенный словарь
3) подключаешь в settings.py в контанте TEMPLATES в ключе context_processors

Если нужна переменная котрая будет обращаться в бд, то луше написать шаблоный тег
или просто inclusion_tag
Контекстные процессоры выполняются при обработке всех запросов использующих RequestContext



----------------------------------------------------------------------------------------------------------
                                файл admin.py


есть два споссоба добавлять классы к админке:

1) через вызов напрямую admin.site.register(SomeModel, SomeModelModelAdmin)

2) через декоратор @admin.register(SomeModel) над классом унаследоавнным от ModelAdmin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated',]
    list_editable = ['price', 'available',]
    prepopulated_fields = {'slug': ('name',),}


list_display - то что мы видим в общем списке

list_filter - те поля, по которым мы можем фильтровать

list_editable - добавляет возможность изменять перечисленные поля со страницы списков

list_editable - добавляет возможность изменять перечисленные поля со страницы списков
но все поля list_editable должны быть обязательно в list_display

prepopulated_fields - словарь, который автоматически преобразует поле (ключ),
по выбранному значению. чаще всего используется для добавления слага через админку


TabularInline
Оень интересная логика у TabularInline. Этот класс позволяет присоединиться к классу с которым связан
по ForeignKey, ManyToMany, OneToOneField

Вот как выглядит
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

см. результат
http://127.0.0.1:8000/admin/orders/order/add/


1) Создаешь в admin.py класс, который наследуется от admin.TabularInline
2) Указываешь в этом классе аттрибут model (с какой моделью будет работать этот класс)
3) Присваиваешь этот класс в списке в аттрибуте inlines
в классе, в котором хочешь, чтобы эта модель отображалась


Добавление собственных действий в сайт администрирования, например
вывод информации из бд в формат csv
https://docs.djangoproject.com/en/3.2/howto/outputting-csv/

Когда мы расширяем стандартные страницы сайта администрирования - нужно знать, какие блоки использует django
блоки в базовом шаблоне сайта администрирования django:
https://github.com/django/django/tree/main/django/contrib/admin/templates/admin

Чтобы переопределить шаблоны django - достаточно воспроизвести иерархию папок
сайта администрирования django в каталоге templates нашего приложения
тогда django будет находить файлы первыми и использовать их

А в остальном смотри в приложении orders
обрати внимание, на то, то мы передали функцию в list_display  - order_detail
посмотри на что эта функция ссылается и все такое

Важно!! запомни декоратор @staff_member_required
Он очень важный для работы с админкой
staff_member_required - проверяет у request.user - is_staff==True и admin==True

from django.contrib.admin.views.decorators import staff_member_required


----------------------------------------------------------------------------------------------------------
                            celery
sources:
https://docs.celeryproject.org/en/stable/

Celery - это очередь событий, которая может решать множество различных задач.
Этот инструмент выполняет задачи из очереди в режиме реального времени
но также позволяет задать расписание

celery позволяет:
-- выполнять трудоемкие процессы в асинхронном режиме
-- инструмент для отложенного выполнения задач по расписанию

queue - очередь (просто слово)

Установка celery - pip install celery (не selery!!!)
дальнейшую установку celery смотри в celery.py

Константа CELERY_ALWAYS_EAGER - позволяет выполнять асинхронные задачи в синхронном режиме
(вместо отправки их в очередь)

Существует договоренность, что асинхронные задачи для celery должны быть расположены в
файле tasks.py одного из приложений
в нашем случае orders/tasks.py


----------------------------------------------------------------------------------------------------------
                        Options

from django.db.models.options import Options

SomeModel._meta - получишь класс экземпляр класса Options этой модели

Очень интересный класс Options. Посмотри на аттрибуты экземпляра, которые создаются в конструкторе
self от Options потом сможет работать с этими аттрибутами (аттрибуты экземпляра класса)
Выглядит так, что он схож с ContentType

Но отличий очень много:

-- Options не имеет таблицы в db
-- Мета данные, которые мы можем получить в Options - более подробные чем в ContentType (посмотри в конструктор)
-- Если нет своей таблицы в бд, то это означает, что данные хранятся в оперативной памяти
а это означает что данные генерируются каждый раз заново, когда мы работаем с Options
Получается что класс Options - читает модель с которой работает

Методов у Options тоже очень много и многие из них крутые

есть метод get_fields() - где ты получаешь кастомный список django
состоящий из полей этой модели
Кстати не забывай - что поля модели это тоже классы python со своими методами и аттрибуами

from django.db.models.fields import related
from django.db.models import fields

from django.db.models import ManyToOneRel
Вот аттрибуты и методы поля ManyToOne (ForeignKey для зависимой модели):
auto_created
concrete
db_type
delete_cached_value
editable
empty_strings_allowed
field
field_name
get_accessor_name
get_cache_name
get_cached_value
get_choices
get_extra_restriction
get_internal_type
get_joining_columns
get_lookup
get_path_info
get_related_field
hidden
identity
is_cached
is_hidden
is_relation
limit_choices_to
many_to_many
many_to_one
model
multiple
name -- дает название поля (как он назван в модели). Аттрибут
null
on_delete
one_to_many
one_to_one
parent_link
related_model
related_name
related_query_name
remote_field
set_cached_value
set_field_name
symmetrical
target_field

Работать с полями модели можно по полной программе.
Очень хороший пример работы с Options и полями модели (а также просто с админкой) -
- смотри в файле orders/admin.py

Options - это отличный класс для работы с meta-data модели, которые не хранятся в db

Вот что написано в конструкторе Options:
# For any class that is a proxy (including automatically created
# classes for deferred (отложенный) object loading), proxy_for_model tells us
# which class this model is proxying. Note that proxy_for_model
# can create a chain of proxy models. For non-proxy models, the
# variable (переменная) is always None.

# For any non-abstract class, the concrete class is the model
# in the end of the proxy_for_model chain. In particular, for
# concrete models, the concrete_model is always the class itself.

# List of all lookups defined in ForeignKey 'limit_choices_to' options
# from *other* models. Needed for some admin checks. Internal use only.

# A custom app registry to use, if you're making a separate model set.

Кстати, класс Options доступен не только для классов моделей (заимствованных от Model)
но и от ModelForm, а возможно даже и от Form

Имхо - Options дает возможность сделать наш код универсальным при работе с моделями,
а не работать нам с конкретно какой-то моделью

смотри на функцию export_to_csv (from orders.admin import export_to_csv)
Отличный пример работы с Options

Да и сам Options переводится как "опции" что хорошо соответствует функции этого класса

Через класс Options можно вызвать класс app_config. Собственно у класса Options какой либо модели есть
атрибут app_config, и через него будет доступен конфигурационный класс нашего приложения

вспоминаем apps.py:

# При создании приложения! django создает определяет конфигурационный класс
# при создании приложения создается файл apps.py где описан базовый конфигурационный класс
# он унаследован от AppConfig - эти классы позволяют нам хранить методанные приложения
# и предоставляют нам интроспекцию
# https://docs.djangoproject.com/en/3.2/ref/applications/

# Интроспекция (англ. type introspection) в программировании — возможность запросить тип
# и структуру объекта во время выполнения программы.

# метод ready() - вызывается сразу как только заполнен реестр приложения
# любая логика связанная с инициализацией нашего приложения должна быть объяснена в этом методе
https://github.com/Kirill67tyar/bookmarks-service/blob/master/src/accounts/draft.py

Таким образом, можно заключить что Options тоже предоставляет нам возможность интроспецкии (как и AppConfig),
но только не приложения, а модели (и довольно широкую интропекцию)



----------------------------------------------------------------------------------------------------------
                        Интернационализация и Локализация

Интернационализация (i18n) - процесс адаптации программы, чтобы она могла использоваться на разных языках
Локализация - приведение (l10n) программы к одному языку
https://www.google.com/search?q=i18n+l10n&newwindow=1&rlz=1C1SQJL_ruRU847RU848&sxsrf=ALeKk03ssCR3q6zpvP6g13_3FZRNhQk82g%3A1621330673021&ei=8YqjYJxZkNfcA4qhusgN&oq=i18n+l10n&gs_lcp=Cgdnd3Mtd2l6EAMyAggAMgUIABDLATICCAAyBQgAEMsBOgcIABBHELADOgcIABCwAxBDOgUIABCxAzoICAAQsQMQgwFQi7tGWKPlRmCK6UZoA3ACeACAAfECiAG_C5IBBzAuNS4xLjGYAQCgAQKgAQGqAQdnd3Mtd2l6yAEKwAEB&sclient=gws-wiz&ved=0ahUKEwjcldC299LwAhWQK3cKHYqQDtkQ4dUDCA4&uact=5
Подсистема интернационализации django поддерживает переводы более чем на 50 языках

Система интернационализации django позволяет пометить строки, которые нужно перевести
и в python коде и в html шаблоне.
Эта система использует возможности утилиты gettext чтобы управлять файлами переводов

Файл перевода - это просто текстовый файл
Он содержит часть строк, которые нужно перевести, и их перевод на конкретный язык
Такие файлы сохраняются с расширеникм .po
После того, как процесс перевод будет окончен получившиеся документы компилируются в файл
с расширением .mo для быстрого поиска переводов

Internationalization
https://docs.djangoproject.com/en/3.2/topics/i18n/

список всех кодов языка:
http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE = 'ru-ru'#'en-us'

TIME_ZONE = 'UTC'# строка задающая временную зону проекта (по умолчанию - 'UTC')

USE_I18N = True# включена ли интернационализация

USE_L10N = True# включена ли локализация для дат, времени и чисел

USE_TZ = True# использовать ли даты с учетом временной зоны


from django.conf import global_settings

В константе LANGUAGES указаны все доступные языки для django
в settings используются в основном константы, и часто эти константы из проекта в проект одни и те же

Чтобы настроить проект на поддержание каких-либо языков нужно создать
тапл LANGUAGES состоящий из доступных языков

LOCALE_PATHS - список путей в файловой системе, по которым django будет находить переводы проекта
LOCALE_PATHS = os.path.join(BASE_DIR, 'locale/')
Как только django находит перый, он прерывает поиск. Если находится в приложении, то
сначала будет искать в приложении, а потом в корне проекта

Полный список настроек для интернационализации
https://docs.djangoproject.com/en/3.2/ref/settings/#globalization-i18n-l10n


from django.utils.translation import gettext as _

Чтобы переводить стоки в python код нужно пометить их как переводимые с помощью функции gettext
from django.utils.translation import gettext as _
Среди разработчиков принято соглашение помечать эту функцию как _

базовые команды gettext:

-- gettext
-- gettext_lazy
-- ngettext
-- ngettext_lazy

1) Базовый вызов функции прост:
from django.utils.translation import gettext as _
output = _('String must be translated')

2) Ленивые переводы (_lazy) выполняются не в момент вызова функции, а когда они понадобятся
Бывает полезен когда строки содержатся в файлах в момент импортирования модулей

3) Иногда нужно применять перевод с именованными переменными, которые динмачески меняются:
month = 'April'
day = 12
output = "Today is %(month)s %(day)" % {'month': month, 'day': day,}

Всегда нужно использовать имнованные аргументы вместо позиционых. Т.к. предложения
на разных языках имеют разную строктуру

4) для перевода строк во множественном числе используется ngettext и ngettext_lazy
эти функции выполняют перевод строк в множественном и единственном числе в зависимости
от количества объекта


Алгоритм работы:
1 -- подключаем {% load i18n %} в нужный шаблон (в начало файла, после extends)
2 -- нужные слова (текст) помечаем тегом {% trans 'must be translated' %}
3 -- может быть такой закрывающий тег. Че он делает - я хз.
    {% blocktrans with some_attribute=from_context.some_attribute ... %}{% endblocktrans %}
4 -- вводим в консоли команду  django-admin makemessages -all
    она соберет все слова помеченные тегом {% trans .. %} и соберет их в файл в папке locale
с расширением .po в переменную msgid (в конце файла)
5 -- обозначить в переменной msgstr то как эти слова нужно перевести
6 -- вводим в консоли команду django-admin compilemessages   она все переведет
    (формирует файлы с расширением .mo который будет использоваться для поиска переводов)

Rosetta - сторонне приложение, которое добавляет возможность редактировать
файлы переводов, через сайты администрирования
С его помощью можно редактировать .po файлы и обновлять .mo файлы.
https://pypi.org/project/django-rosetta/
https://django-rosetta.readthedocs.io/
pip install django-rosetta

сайт для rosetta когда она уже установлена:
http://127.0.0.1:8000/rosetta/


Что есть файл с расширением .po
https://ru.opensuse.org/openSUSE:%D0%9F%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4_PO_%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2
Все тексты что должны быть переведены (диалоги, меню и т.д...), сохраняется в PO файл.
PO файл - это файл перевода для приложения, с расширением .po и со специальной структурой
содержащей: информацию о языке, переводчике, оригинальные диалоги и их переводы.
Оригинальные диалоги начинаются с msgid, за ними следуют строки msgstr "текст перевода".
Информацию о языке и переводчике находится в начале PO файла. Если для диалога нет перевода,
оставьте msgstr пустым. Строки начинающиеся с символа # являются комментариями.


Как сделать так, чтобы Django автоматически определял какой язык нужно использовать?
from django.conf.urls.i18n import i18n_patterns
в базовом urls.py заменить list на функцию i18n_patterns
urlpatterns = i18n_patterns( path(...),
                                path(...),)
django будет определять какой язык по заголовку Accept-Language
http запроса (request) какой посылает браузер
Если определить не ссможет (что маловероятно) то будет использовать код из константы LANGUAGE_CODE
в начало (но скорее всего после ip:tcp)url будет добавляться специальный языковой префикс /en/ (/ru/)
в зависимсти от языка.
За это действие отвечает промежуточный слой 'django.middleware.locale.LocaleMiddleware'
в MIDDLEWARE


Можно также использовать приложение Poedit
https://poedit.net/
Доступно для Windows, MacOS, Linux

В целом об этой теме и вообще логике работы интернационализации и локализации Django
читай Антонио Меле - Django 2 в примерах, стр. 267 - 294

Ну а если надо перевести слова нормально, со смыслом, для этого хорошо подходит django-parler
https://django-parler.readthedocs.io/en/stable/
https://github.com/django-parler/django-parler

Позволяет нам работать как с моделями, так и с админкой.
С моделями создает таблицу ManyToOne с переводом, кодом языка, внешним ключем
на запись которую переводим (вообщем смотри в таблицу    нынешней db)

Но стоит учитывать, что django-parler накладывает определенные ограничения:
https://django-parler.readthedocs.io/en/stable/compatibility.html#

Нельзя указывать в мета классе модели ordering, index_together

Короче, django-parler - ебучая библиотека, с кучей багов и костылей, нафиг она нужна.
"""
from django.conf import global_settings
from django.db.models import ManyToOneRel, Manager
from django.middleware.locale import LocaleMiddleware
from django.db.models.fields import related

'django.middleware.locale.LocaleMiddleware'
from django.db.models.options import Options
# Минутка философии
# когда создаешь какой-нибудь класс, подумай - целесообразно ли создавать класс чтобы там
# был полный функционал CRUD для объекта. Иногда бывает целесообразно, иногда нет.
# Дальше, если целесообразно, то строй ответвления
# Creat - что создавать, какой должен быть объект.
# Read - что показывать, какой объект или параметры. что нужно показать.
# (очень асто функционалу Read нужен итератор, чтобы наш класс мог итерироваться)
# Update - что изменить, опять же, какие параметры (аттрибуты). полностью ли объект изменить, или частично.
# Creat - что удалить и как.
# очень хороший пример CRUD функционала - cart/cart.py - класс Cart
# для работы с сессиями.

# Рекомендуется (почему - не знаю) передавать в аргументы обработчиков, если мы хотим работать с моделью,
# идентификаторы. А получать сами объекты из бд лишь во время выполнения задачи (кода обработчика)
# обрати внимание, что во всех обработчиках мы так и делаем

# Интернационализация (i18n) - процесс адаптации программы, чтобы она могла использоваться на разных языках
# Локализация - приведение (l10n) программы к одному языку
# https://www.google.com/search?q=i18n+l10n&newwindow=1&rlz=1C1SQJL_ruRU847RU848&sxsrf=ALeKk03ssCR3q6zpvP6g13_3FZRNhQk82g%3A1621330673021&ei=8YqjYJxZkNfcA4qhusgN&oq=i18n+l10n&gs_lcp=Cgdnd3Mtd2l6EAMyAggAMgUIABDLATICCAAyBQgAEMsBOgcIABBHELADOgcIABCwAxBDOgUIABCxAzoICAAQsQMQgwFQi7tGWKPlRmCK6UZoA3ACeACAAfECiAG_C5IBBzAuNS4xLjGYAQCgAQKgAQGqAQdnd3Mtd2l6yAEKwAEB&sclient=gws-wiz&ved=0ahUKEwjcldC299LwAhWQK3cKHYqQDtkQ4dUDCA4&uact=5
# Подсистема интернационализации django поддерживает переводы более чем на 50 языках

# from django.template.context_processors import request
# request - экземляр класса HttpRequest
# посмотреть на него можно здесь:
# from django.http.request import HttpRequest, QueryDict


# ччто есть PositiveIntegerField?
# Допустим
# quantity = PositiveIntegerField()
# SQL команда будет:
# "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0)

# класс HttpResponse намного больше чем просто вывести что-то на страницу
# с помощью HttpResponse можно определить content_type и другие заголовки
# при формировании response
# Посмотри как он устроен, какие аргументы туда передаются:
# from django.http import HttpResponse
# Это очень класс, позволяющий гибкие инстументы для формирования своего response


# Функцию mark_safe нужно использовать, чтобы избежать пропуска HTML тегов
# Важно не использовать эту функцию для данных введеных пользователями сайта
# так как пользователь может ввести html код
# from django.utils.safestring import mark_safe

# Очень крутая функция django - render_to_string
from django.template.loader import render_to_string
# Посмотри, какие аргументы она принимает
# Передаешь template_name. Передаешь котнекст для этого шаблона
# и эта функция преобразует этот шаблон в объект python - str.

# Библиотека python для работы с PDF - Reportlab

# Что даст python --version --version  huh?
# $ python --version --version
# Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 21:26:53) [MSC v.1916 32 bit (Intel)]





# А что насчет скидок? здесь можно использовать IntegerField с именованным аргументов validators
# а в validators мы передаем список с двумя валидаторами
# выглядит все так:

# from django.core.validators import MinValueValidator, MaxValueValidator
# discount = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100), ], verbose_name='Скидка')

# Теперь известно что и у models могут быть свои валидаторы (а не только у forms).
# благодаря валидаторам MinValueValidator(0) и MaxValueValidator(100)
# мы не можем ввести значение <0 и >100. Наш discount может быть строго 0<=discount<=100
# Обрати внимание что это модель а не форма, а аргумент validators есть