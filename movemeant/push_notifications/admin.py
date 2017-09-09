from django.contrib import admin

from .models import PushNotification, Device


class DevicesAdmin(admin.ModelAdmin):
    list_display = ('user', 'condition')


class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'device', 'time_created')


admin.site.register(Device, DevicesAdmin)
admin.site.register(PushNotification, PushNotificationAdmin)
