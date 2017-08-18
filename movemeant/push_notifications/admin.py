from django.contrib import admin

from .models import PushNotification

class PushNotificationAdmin(admin.ModelAdmin):
    model = PushNotification
    # list_display = ('name', '_total_members', '_total_venues', '_total_reveals', 'time_modified', 'time_created',)

admin.site.register(PushNotification, PushNotificationAdmin)