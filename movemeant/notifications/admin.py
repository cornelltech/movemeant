from django.contrib import admin
from notifications.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('id', 'title', 'text', 'time_created')
    list_filter = ('time_created',)

admin.site.register(Notification, NotificationAdmin)