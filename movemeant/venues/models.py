from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Cohort(models.Model):
    name = models.CharField(max_length=500)
    members = models.ManyToManyField(User, blank=True)

    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        ordering = ('time_created',)
    
    def get_member_count(self):
        return self.members.all().count()


class Region(models.Model):
    zipcode = models.CharField(max_length=100)
    cohort = models.ForeignKey(Cohort)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{zipcode}'.format(zipcode=self.zipcode,)
    class Meta:
        ordering = ('time_created',)    


class Venue(models.Model):
    foursquare_id = models.CharField(max_length=500)

    name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=200, blank=True)

    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        ordering = ('time_created',)
    
    def get_total_visits(self):
        visits = 0
        venueCheckins = self.venuecheckin_set.all() 
        for checkin in venueCheckins:
            visits += checkin.count 
        return visits
    
    def get_total_reveals(self):
        return self.venuereveal_set.all().count()


class VenueCheckin(models.Model):
    cohort = models.ForeignKey(Cohort)
    venue = models.ForeignKey(Venue)

    count = models.IntegerField(default=0)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('time_created',)


class VenueReveal(models.Model):
    cohort = models.ForeignKey(Cohort)
    participant = models.ForeignKey(User)
    venue = models.ForeignKey(Venue)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('time_created',)
