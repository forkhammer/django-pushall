from django.contrib import admin
from .models import PushUser


class PushallUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uid')
    list_per_page = 50

admin.site.register(PushUser, PushallUserAdmin)
