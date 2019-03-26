# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sign.models import Event, Guest


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    search_fields = ['name']
    list_filter = ['status']

class GuessAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time']
    search_fields = ['realname','phone']
    list_filter = ['sign']


admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuessAdmin)
# Register your models here.
