from rest_framework import serializers

from venues.models import Cohort, Region, Venue


class CohortSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Cohort
        fields = ('id', 'name', 'member_count', 'time_created', 'time_modified',)
    
    def get_member_count(self, obj):
        return obj.get_member_count()


class VenueSerializer(serializers.ModelSerializer):
    foursquare_id = serializers.CharField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    category = serializers.CharField(allow_null=True)

    class Meta:
        model = Venue
        fields = ('id', 'name', 'foursquare_id', 'category', 'time_created', 'time_modified',)
    
