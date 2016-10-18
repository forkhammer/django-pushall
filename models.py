from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .app_settings import *
import requests, json


class PushUser(models.Model):
    user = models.ForeignKey(USER_MODEL, verbose_name=_('User'), default=None, blank=True, null=True,
                             related_name='subscribers')
    uid = models.CharField(_('PushAll ID'), max_length=100, default='')
    date = models.DateTimeField(_('Date subscribe'), default=timezone.now)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')

    def notice(self, title, text, url=None, icon=None, ttl=None):
        return PushAll.unicast(self.uid, title, text, url, icon, ttl)

    @staticmethod
    def notice_to_user(user, title, text, url=None, icon=None, ttl=None):
        uids = [u.uid for u in user.subscribers.all()]
        return PushAll.multicast(uids, title, text, url, icon, ttl)


class PushAllAPI(object):
    def _send(self, type, id, key, title, text, url=None, icon=None, ttl=None, **kwargs):
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
        return response.get('success', 0) > 0

    def self(self, title, text, url=None, icon=None, ttl=None):
        if not PUSHALL_USER_ID:
            raise Exception('Не указан PUSHALL_USER_ID')
        if not PUSHALL_USER_KEY:
            raise Exception('Не указан PUSHALL_USER_KEY')
        return self._send('self', PUSHALL_USER_ID, PUSHALL_USER_KEY, title, text, url, icon, ttl)

    def broadcast(self, title, text, url=None, icon=None, ttl=None):
        return self._send('broadcast', PUSHALL_CANAL_ID, PUSHALL_API_KEY, title, text, url, icon, ttl)

    def multicast(self, uids, title, text, url=None, icon=None, ttl=None):
        return self._send('multicast', PUSHALL_CANAL_ID, PUSHALL_API_KEY, title, text, url, icon, ttl, uids=json.dumps(uids))

    def unicast(self, uid, title, text, url=None, icon=None, ttl=None):
        return self._send('unicast', PUSHALL_CANAL_ID, PUSHALL_API_KEY, title, text, url, icon, ttl, uid=uid)


PushAll = PushAllAPI()