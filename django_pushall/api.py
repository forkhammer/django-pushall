#-*- coding: utf-8 -*-
from .app_settings import *
import requests
import json


class PushallAPI(object):
    def _send(self, type, id, key, title=None, text=None, url=None, icon=None, ttl=None, **kwargs):
        data = {
            'type': type,
            'id': id,
            'key': key,
            'title': title,
            'text': text,
            'url': url,
            'icon': icon,
            'ttl': ttl
        }
        data.update(kwargs)
        r = requests.post(PUSHALL_API_URL, data=data)
        response = json.loads(r.text)
        if response.get('error', None):
            raise Exception(response.get('error', None))
        if response.get('success', 0) > 0:
            return response.get('lid', None)
        else:
            return None

    def _check_self(self):
        if not PUSHALL_USER_ID:
            raise Exception('Не указан PUSHALL_USER_ID')
        if not PUSHALL_USER_KEY:
            raise Exception('Не указан PUSHALL_USER_KEY')

    def _check_canal(self):
        if not PUSHALL_CANAL_ID:
            raise Exception('Задайте PUSHALL_CANAL_ID')
        if not PUSHALL_API_KEY:
            raise Exception('Задайте PUSHALL_API_KEY')

    def self(self, title, text, url=None, icon=None, ttl=None):
        """
        Send notice to myself
        :param title:
        :param text:
        :param url:
        :param icon:
        :param ttl:
        :return:
        """
        self._check_self()
        return self._send('self', PUSHALL_USER_ID, PUSHALL_USER_KEY, title, text, url, icon, ttl)

    def broadcast(self, title, text, url=None, icon=None, ttl=None):
        """
        Send broadcast notice
        :param title:
        :param text:
        :param url:
        :param icon:
        :param ttl:
        :return:
        """
        self._check_canal()
        return self._send('broadcast', PUSHALL_CANAL_ID, PUSHALL_API_KEY, title, text, url, icon, ttl)

    def multicast(self, uids, title, text, url=None, icon=None, ttl=None):
        """
        Send notice to users from uids list
        :param uids:
        :param title:
        :param text:
        :param url:
        :param icon:
        :param ttl:
        :return:
        """
        self._check_canal()
        return self._send('multicast', PUSHALL_CANAL_ID, PUSHALL_API_KEY, title, text, url, icon, ttl, uids=json.dumps(uids))

    def unicast(self, uid, title, text, url=None, icon=None, ttl=None):
        """
        Send notice to user with uid
        :param uid:
        :param title:
        :param text:
        :param url:
        :param icon:
        :param ttl:
        :return:
        """
        self._check_canal()
        return self._send('unicast', PUSHALL_CANAL_ID, PUSHALL_API_KEY, title, text, url, icon, ttl, uid=uid)

    def show_list(self, lid=None):
        """
        Get channel feed
        :param lid:
        :return:
        """
        self._check_canal()
        data = {
            'type': 'showlist',
            'id': PUSHALL_CANAL_ID,
            'key': PUSHALL_API_KEY,
            'lid': lid,
        }
        r = requests.post(PUSHALL_API_URL, data=data)
        response = json.loads(r.text)
        return response

    def show_users(self, uid=None):
        """
        Get user list or user with uid
        :param uid:
        :return:
        """
        self._check_canal()
        data = {
            'type': 'showlist',
            'subtype': 'users',
            'id': PUSHALL_CANAL_ID,
            'key': PUSHALL_API_KEY,
            'uid': uid,
        }
        r = requests.post(PUSHALL_API_URL, data=data)
        response = json.loads(r.text)
        return response
