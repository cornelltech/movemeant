from django.contrib import admin
from events.models import Event

class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('trigger', 'participant', 'time_created')
    list_filter = ('time_created',)

admin.site.register(Event, EventAdmin)