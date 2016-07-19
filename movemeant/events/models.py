from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class Event(models.Model):
    trigger = models.CharField(max_length=500)
    participant = models.ForeignKey(User, blank=True)

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        ordering = ('time_created',)