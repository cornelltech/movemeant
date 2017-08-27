from __future__ import absolute_import, unicode_literals
from random import choice

from celery import shared_task

from .models import Device

from push_notifications.models import PushNotification
from venues.models import VenueCheckin


@shared_task
def condition_a_check():
    for user in [d.user for d in
                 Device.objects.filter(condition='cond_a')]:  # so that every user's in condition a community is checked

        user_device = user.device_set.all().first()
        user_cohort = user.cohort_set.all().first()

        for venue_checkin in VenueCheckin.objects.filter(cohort=user_cohort):
            if venue_checkin.count > 5:  # type 1
                message_choices = [
                    "5 people from {cohort_name} also went to {venue_name}!".format(
                        cohort_name=user_cohort.name,
                        venue_name=venue_checkin.venue.name
                    ),
                    "You're part of a trend! {cohort_name} people are flocking to {venue_name}.".format(
                        cohort_name=user_cohort.name,
                        venue_name=venue_checkin.venue.name
                    )
                ]
                # send a notification to the current user
                message_selected = choice(message_choices)
                PushNotification.objects.create(
                    title=message_selected,
                    message=message_selected,
                    device=user_device
                )
                break  # breaks the inner loop and goes to the next user
            if venue_checkin.count > 10:  # type 2
                # get list of users that have visited this place (venue) more than 10 times
                # and send a notifications to all those users
                cohort = venue_checkin.cohort
                current_cohort_users = cohort.members

                for user in current_cohort_users:
                    message_choices = [
                        "Have you been to {venue_name} yet? It's trending among {cohort_name} people.".format(
                            cohort_name=user_cohort.name,
                            venue_name=venue_checkin.venue.name
                        ),
                        "Check out {venue_name}, a popular place for {cohort_name} people.".format(
                            cohort_name=user_cohort.name,
                            venue_name=venue_checkin.venue.name
                        )
                    ]
                    current_user_device = user.device_set.all().first()
                    message_selected = choice(message_choices)
                    PushNotification.objects.create(
                        title=message_selected,
                        message=message_selected,
                        device=current_user_device
                    )
                    break

        # by the time we are here, it means the user hasn't received any notifications so far, today.
        # checking the last time he received a notification, will allow us
        # to send him an "open the app" reminder notification
        message_choices = [
            "People from {cohort_name} are going to the same places as you! Open the app to learn more".format(
                cohort_name=user_cohort.name
            ),
            "Your locations are similar to other people in {cohort_name} - Open the app to learn more".format(
                cohort_name=user_cohort.name
            )
        ]
        current_user_device = user.device_set.all().first()
        message_selected = choice(message_choices)
        PushNotification.objects.create(
            title=message_selected,
            message=message_selected,
            device=current_user_device
        )


@shared_task
def condition_b_check():
    for user in [d.user for d in
                 Device.objects.filter(condition='cond_b')]:  # so that each user in condition b get's a notification

        user_device = user.device_set.all().first()
        user_visited_venues = VenueCheckin.objects.filter(cohort__members__username__contains=user.username)

        for v in user_visited_venues:
            if v.count > 3:
                message = "{venue_name} is one of your go-to places".format(venue_name=v.venue.name)
                PushNotification.objects.create(
                    title=message,
                    message=message,
                    device=user_device
                )

