from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import Device

from venues.models import VenueCheckin


@shared_task
def condition_a_check():
    for user in [d.user for d in
                 Device.objects.filter(condition='cond_a')]:  # so that every user's in condition a community is checked
        user_cohort = user.cohort_set.all().first()

        for venue_checkin in VenueCheckin.objects.filter(cohort=user_cohort):
            if venue_checkin.count > 5:  # type 1
                # todo
                # send a notification eg. "5 people from [Cohort Name] also went to X!"
                # to the current user
                pass
            if venue_checkin.count > 10:  # type 2
                # get list of users that have visited this place (venue) more than 10 times
                cohort = venue_checkin.cohort
                users = cohort.members

                # todo
                # send a notifications to all those users
                # "Have you been to X yet? It's trending among [Cohort Name] people."


@shared_task
def condition_b_check():
    for user in [d.user for d in
                 Device.objects.filter(condition='cond_b')]:  # so that each user in condition b get's a notification
        user_visited_venues = VenueCheckin.objects.filter(cohort__members__username__contains=user.username)
        for v in user_visited_venues:
            if v.count > 3:
                # todo
                # send a notification "X is one of your go-to places"
                pass
