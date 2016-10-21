from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .app_settings import *


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
        from . import Pushall
        return Pushall.unicast(self.uid, title, text, url, icon, ttl)

    @staticmethod
    def notice_to_user(user, title, text, url=None, icon=None, ttl=None):
        from . import Pushall
        uids = [u.uid for u in user.subscribers.all()]
        return Pushall.multicast(uids, title, text, url, icon, ttl)
