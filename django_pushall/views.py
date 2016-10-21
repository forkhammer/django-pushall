from django.views.generic import View
import hashlib
from django.shortcuts import HttpResponseRedirect
from .app_settings import *
from .models import PushUser


class CallbackView(View):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get('pushalluserid', '')
        time = request.GET.get('time', '')
        sign = request.GET.get('sign', '')
        ip = request.META['REMOTE_ADDR']
        hash = hashlib.md5()
        hash.update((PUSHALL_API_KEY + uid + time + ip).encode('utf8'))
        if sign != hash.hexdigest():
            raise Exception('Invalid sign')

        exists = PushUser.objects.filter(uid=uid)
        if not exists:
            pu = PushUser(uid=uid)
            if request.user.is_authenticated():
                pu.user = request.user
            pu.save()
        return HttpResponseRedirect(redirect_to=PUSHALL_CALLBACK_REDIRECT)
