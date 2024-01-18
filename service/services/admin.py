from django.contrib import admin

from services.models import Subscribtion, Service, Plan

admin.site.register(Service)
admin.site.register(Subscribtion)
admin.site.register(Plan)