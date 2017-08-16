from __future__ import unicode_literals

from random import choice

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_str


class Device(models.Model):
    cond_a = 'cond_a'
    cond_b = 'cond_b'
    CONDITIONS = (
        (cond_a, 'Condition A'),
        (cond_b, 'Condition B')
    )

    user = models.ForeignKey(to=User)
    token = models.CharField(max_length=250)
    condition = models.CharField(max_length=6, choices=CONDITIONS)

    def __str__(self):
        return smart_str("{} - {}".format(self.user.username, self.token))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.condition = choice(['cond_a', 'cond_b'])

        super(Device, self).save(force_insert, force_update, using, update_fields)


class PushNotification(models.Model):
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=250)
    devices = models.ManyToManyField(Device)

    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return smart_str("{} - {} devices".format(self.title, self.devices.count()))
