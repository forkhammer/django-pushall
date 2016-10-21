# django-pushall
django-pushall - это приложение для поддержки системы Push-уведомлений PushAll для фреймворка Django.
Подробное описание системы PushAll на [официальном сайте](https://pushall.ru)

Поддерживает версии Django>=1.8, Python 2.7, 3.4, 3.5

#Установка
Добавить приложение в _INSTALLED_APPS_

    INSTALLED_APPS = [
        ...
        'django-pushall',
        ... 
    ]    

Выполнить команду

    python manage.py migrate
    
для создания таблиц моделей

Если вы будете использовать [Callback](https://pushall.ru/blog/api) для определения подписавшихся пользователей,
то необходимо добавить в _urls.py_

    urlpatterns = [
        ...
        url(r'^pushall/', include('django_pushall.urls')),
        ...
    ]
    
Укажите настройки канала в _settings.py_

    PUSHALL_CANAL_ID = 1234
    PUSHALL_API_KEY = 'e789ed7bea3cbd86e951e4b268b45ed8'

_PUSHALL_CANAL_ID_ - идентификатор канала. _PUSHALL_API_KEY_ - ключ API канала на [Pushall.ru](Pushall.ru)
Вы получите эти настройки при создании канала на сайте

Если вы планируете отправлять уведомления самому себе, то укажите в _settings.py_

    PUSHALL_USER_ID = 01234
    PUSHALL_USER_KEY = '3c2f2dc68c59b65ba9c789fd3a3fb4f6'
    
_PUSHALL_USER_ID_ - идентификатор вашей учетной записи на сайте [Pushall.ru](Pushall.ru).
_PUSHALL_USER_KEY_ - ключ API вашей учетной записи
Получить эти настройки можно в личном кабинете на сайте _Pushall.ru -> Администрирование -> API общее_

#Отправка уведомлений
##Отправка самому себе

    from django_pushall import Pushall
    
    Pushall.self('Заголовок', 'Текст сообщения')  # простое уведомление
    Pushall.self('Заголовок', 'Текст сообщения', url='http://site.ru')  # уведомление со ссылкой
    Pushall.self('Заголовок', 'Текст сообщения', icon='http://site.ru/icon.png')  # уведомление со своей иконкой
    Pushall.self('Заголовок', 'Текст сообщения', ttl=2160000)  # уведомление со временем жизни в секундах
    
Метод _Pushall.self_ возвращает идентификатор уведомления
    
##Отправка всех пользователям канала

    from django_pushall import Pushall
    
    Pushall.broadcast('Заголовок', 'Текст сообщения')
    
Параметры ссылки, иконки и времени жизни аналогичны предыдущему пункту.
Возвращает идентификатор уведомления.

##Отправка подписчику канала

    from django_pushall import Pushall
    
    Pushall.unicast(12345, 'Заголовок', 'Текст сообщения') #отправка уведомления подписчику с идентификатором 12345
    
Параметры ссылки, иконки и времени жизни аналогичны предыдущему пункту.
Возвращает идентификатор уведомления

##Отправка нескольким подписчикам канала

    from django_pushall import Pushall
    
    Pushall.milticast([12345, 12346, 12347], 'Заголовок', 'Текст сообщения') #отправка уведомления подписчикам с идентификаторами 12345, 12346, 12347
    
Параметры ссылки, иконки и времени жизни аналогичны предыдущему пункту.
Возвращает идентификатор уведомления

##Просмотр состояния ленты канала

    from django_pushall import Pushall
    
    print(Pushall.show_list()) #вывод на экран состояния ленты канала
    print(Pushall.show_list(lid=1000)) #вывод на экран состояния уведомления c идентификатором 1000
    
##Просмотр списка подписчиков канала
    
    from django_pushall import Pushall

    print(Pushall.show_users()) #вывод на экран списка подписчиков
    print(Pushall.show_users(uid=12345)) #вывод на экран информации о подписчике с идентификатором 12345
    
#Сбор подписчиков
Чтобы приложение знало какие пользователи подписались на ваш канал необходимо использовать Callback подписки.
Для этого необходимо добавить в _urls.py_

    urlpatterns = [
        ...
        url(r'^pushall/', include('django_pushall.urls')),
        ...
    ]
    
и указать в настройках канала на сайте Pushall.ru **Callback-адрес для получения ID**

    http://ваш-url/pushall/callback
    
После подписки пользователь будет переходить по этому адресу. Приложение получит его UID в системе и далее перенаправит на главную страницу вашего сайта
Изменить адрес редиректа можно в _setting.py_

    PUSHALL_CALLBACK_REDIRECT = 'адрес редиректа'
    
Все подписчики привязываются к пользователям сайта.
Получить список подписчиков можно так

    from django_pushall.models import PushUser
    
    subscribers = PushUser.objects.all()
    
##Отправить уведомление подписчику

    from django_pushall.models import PushUser
    
    subscriber = PushUser.objects.get(uid=12345)
    subscriber.notice('Заголовок', 'Текст')
    
Можно использовать параметры **icon, url, ttl**

##Отправить уведомление пользователю сайта

    from django.contrib.auth.models import User
    from django_pushall.models import PushUser
    
    user = User.objects.get(id=1)
    PushUser.notice_to_user(user, 'Заголовок', 'Текст')
    
