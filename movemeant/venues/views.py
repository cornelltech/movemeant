from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from venues.models import Cohort, Region, Venue, VenueCheckin, VenueReveal
from venues.serializers import CohortSerializer, VenueSerializer
from venues.foursquare import search as geo_search
from events.models import Event


class CohortViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer


class VenueMineCohortLogAPIHandler(APIView):
    """
    Given a list of Location ids return the basic info for that list
            @params Ids of coords
            @example localhost:8000/api/v1/locations?ids=1,2,3,4
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        cohort = request.user.cohort_set.all().first()

        try:
            ids = [ int(id) for id in request.query_params.get('ids', '').split(',') ]
            venues = Venue.objects.filter( id__in=ids )

            logs = []

            for venue in venues:
                venue_checkin = VenueCheckin.objects.filter(cohort=cohort, venue=venue).first() 
                if venue_checkin:
                    logs.append({
                        'id': venue.id,
                        'foursquare_id': venue.foursquare_id,
                        'name': venue.name,
                        'category': venue.category,
                        'lat': venue.lat,
                        'lng': venue.lng,

                        'checkins': venue_checkin.count,
                        
                        'reveals': venue.get_total_reveals(cohort),
                        'revealed': venue.is_user_revealed(user),
                        'revealed_users': venue.get_revealed_users(cohort)
                    })    
                else:
                    continue

            return Response(logs, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


class VenueCohortLogAPIHandler(APIView):
    """
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        response = {
            'results': [],
            'count': 0
        }

        user = request.user
        cohort = request.user.cohort_set.all().first()

        # get all the venuecheckins for the user's cohort
        checkins = VenueCheckin.objects.filter(cohort=cohort)
        for checkin in checkins:

            response['results'].append({
                'id': checkin.venue.id,
                'foursquare_id': checkin.venue.foursquare_id,
                'name': checkin.venue.name,
                'category': checkin.venue.category,
                'lat': checkin.venue.lat,
                'lng': checkin.venue.lng,

                'checkins': checkin.count,

                'reveals': checkin.venue.get_total_reveals(cohort),
                'revealed': checkin.venue.is_user_revealed(user),
                'revealed_users': checkin.venue.get_revealed_users(cohort)
            })
        response['count'] = len(response['results'])
        response['cohort'] = cohort.name

        return Response(response, status=status.HTTP_200_OK)


class VenueSearchAPIHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        cohort = request.user.cohort_set.all().first()

        lat = self.request.data.get('lat', None)
        lng = self.request.data.get('lng', None)

        if lat and lng:
            geo_lookup_results = geo_search(lat, lng)

            if geo_lookup_results:
                print geo_lookup_results

                venue, created = Venue.objects.get_or_create(
                    foursquare_id = geo_lookup_results['foursquare_id']
                )

                venue.name = geo_lookup_results['name']
                venue.category = geo_lookup_results['category']
                venue.lat = geo_lookup_results['lat']
                venue.lng = geo_lookup_results['lng']
                venue.save()

                venue_serializer = VenueSerializer(venue)

                return Response(venue_serializer.data, status=status.HTTP_200_OK)
                
            else:
                # no valid venue found

                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            # we need lat/lng
            return Response(status=status.HTTP_400_BAD_REQUEST)


class VenueCheckinAPIHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        cohort = request.user.cohort_set.all().first()

        venue_id = self.request.data.get('venue_id', None)
        
        if venue_id:
            venue = get_object_or_404(Venue, pk=venue_id)
    
            # log the visit
            checkin, created = VenueCheckin.objects.get_or_create(
                cohort = cohort,
                venue = venue
            )
            checkin.count = checkin.count + 1;
            checkin.save()

            Event.objects.create(trigger="venue_checkin_pass", participant=user)

            return Response(status=status.HTTP_200_OK)

        else:
            # we need venue_id
            Event.objects.create(trigger="venue_checkin_fail", participant=user)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class VenueRevealAPIHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):

        user = request.user
        cohort = request.user.cohort_set.all().first()
        venue_id = request.data.get('venue_id', None)

        if venue_id:
            venue = get_object_or_404(Venue, pk=venue_id) 

            VenueReveal.objects.get_or_create(
                cohort = cohort,
                participant = user,
                venue = venue
            )

            response = {
                'id': venue.id,
                'foursquare_id': venue.foursquare_id,
                'name': venue.name,
                'category': venue.category,
                'lat': venue.lat,
                'lng': venue.lng,

                'checkins': 0,
                'reveals': venue.get_total_reveals(cohort)
            }

            Event.objects.create(trigger="venue_reveal_pass", participant=user)

            return Response(response, status=status.HTTP_200_OK)
                    
        else:
            
            Event.objects.create(trigger="venue_reveal_fail", participant=user)

            return Response(status=status.HTTP_400_BAD_REQUEST)
