from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from venues.models import Cohort


class Notification(models.Model):
    cohort = models.ManyToManyField(Cohort)
    
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100, blank=True)

    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('time_created',)


@receiver(post_save, sender=Notification)
def dispatch_notification(sender, instance=None, created=False, **kwargs):
    if created:
        print "*"*50
        print "DISPATCH"

