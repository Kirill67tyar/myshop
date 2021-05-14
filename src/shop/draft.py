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

Очень интересный класс Options. Посмотри на аттрибуты экземпляра, которые создаются конструкторе
self от Options потом сможет работать с этими аттрибутами (аттрибуты кземпляра класса)
Выглядит так, что он схож с ContentType

Но отличий очень много:

-- Options не имеет таблицы в db
-- Мета данные, которые мы можем получить в Options - более подробные чем в ContentType (посмотри в конструктор)
-- Если нет своей таблицы в бд, то это означает, что данные хранятся в оперативной памяти
а это означает то данные генерируются каждый раз заново, когда мы работаем с Options
Получается что класс Options - читает модель с которой работает

Методов у Options тоже очень много и все многие из них крутые

есть метод get_fields() - где ты получаешь кастомный список django
состоящий из полей этой модели
Кстати не забывай - что поля модели это тоже классы python со своими методами и аттрибуами

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


"""
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
