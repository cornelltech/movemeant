from __future__ import unicode_literals

import json
import requests
from random import choice

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    device = models.ForeignKey(Device, null=True)

    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return smart_str("{} - {}".format(self.title, self.device))


@receiver(post_save, sender=PushNotification)
def issue_push_notification(sender, instance, **kwargs):
    tokens = [instance.device.token]
    response = requests.post(
        'https://api.ionic.io/push/notifications',
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + settings.IONIC_TOKEN
        },
        data=json.dumps({
            "tokens": tokens,
            "profile": "push_notifications",
            "notification": {
                "title": instance.title,
                "message": instance.message
            }
        }))
    print response.text
