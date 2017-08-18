from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

from venues.models import Cohort


class Event(models.Model):
    trigger = models.CharField(max_length=500)
    participant = models.ForeignKey(User, blank=True)

    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('time_created',)
