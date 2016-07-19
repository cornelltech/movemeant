from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from venues.models import Cohort, Region
from events.models import Event


class MeAPIHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        cohort = user.cohort_set.all().first()

        response = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'cohort': cohort.name if cohort else '' 
        } 

        Event.objects.create(trigger="application_opened", participant=user)

        return Response(response, status=status.HTTP_200_OK)

class UserCreateAPIHandler(APIView):
    def post(self, request, format=None):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        if username and email and password:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            Event.objects.create(trigger="participant_created", participant=user)
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AffiliateUserWithRegionAPIHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        zipcode = request.data.get('zipcode', None)
        if zipcode:
            region = get_object_or_404(Region, zipcode=zipcode)
            cohort = region.cohort

            cohort.members.add(user)
            response = {
                'cohort': cohort.name
            }
            
            Event.objects.create(trigger="cohort_association_pass", participant=user)

            return Response(response, status=status.HTTP_200_OK)

        else:

            Event.objects.create(trigger="cohort_association_fail", participant=user)

            return Response(status=status.HTTP_400_BAD_REQUEST)