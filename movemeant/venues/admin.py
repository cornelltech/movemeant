from django.contrib import admin

from venues.models import Cohort, Region, Venue, VenueCheckin, VenueReveal


class RegionInLine(admin.TabularInline):
    model = Region
    extra = 1


class CohortAdmin(admin.ModelAdmin):
    model = Cohort
    list_display = ('name', '_total_members', '_total_venues', '_total_reveals', 'time_modified', 'time_created',)
    inlines = [
        RegionInLine,
    ]
    def _total_members(self, obj):
        return obj.get_member_count()

    def _total_venues(self, obj):
        return obj.get_venue_count()
    
    def _total_reveals(self, obj):
        return obj.get_reveal_count()


class VenueAdmin(admin.ModelAdmin):
    model = Venue
    list_display = ('foursquare_id', 'name', 'category', 'lat', 'lng', '_total_visits', '_total_reveals', 'time_created',)
    list_display_links = ('foursquare_id',)
    list_filter = ('category',)

    def _total_visits(self, obj):
        return obj.get_total_visits()
    
    def _total_reveals(self, obj):
        return obj.get_total_reveals()


class VenueCheckinAdmin(admin.ModelAdmin):
    model = VenueCheckin
    list_display = ('cohort', 'venue', 'count', 'time_created',)
    list_filter = ('cohort__name', 'venue',)

class VenueRevealAdmin(admin.ModelAdmin):
    model = VenueReveal
    list_display = ('cohort', 'participant', 'venue', 'time_created',)
    list_filter = ('cohort__name', 'participant__username', 'venue',)



admin.site.register(Cohort, CohortAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(VenueCheckin, VenueCheckinAdmin)
admin.site.register(VenueReveal, VenueRevealAdmin)