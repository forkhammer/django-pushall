#-*- coding: utf-8 -*-
from django.conf import settings

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

PUSHALL_USER_ID = getattr(settings, 'PUSHALL_USER_ID', None)
PUSHALL_USER_KEY = getattr(settings, 'PUSHALL_USER_KEY', None)

PUSHALL_CANAL_ID = getattr(settings, 'PUSHALL_CANAL_ID', None)

PUSHALL_API_KEY = getattr(settings, 'PUSHALL_API_KEY', None)

PUSHALL_API_URL = 'https://pushall.ru/api.php'

PUSHALL_CALLBACK_REDIRECT = getattr(settings, 'PUSHALL_CALLBACK_REDIRECT', '/')