from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from venues.models import Cohort, Region


class MeAPIHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        response = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        } 
        return Response(response, status=status.HTTP_200_OK)

class UserCreateAPIHandler(APIView):
    def post(self, request, format=None):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        if username and email and password:
            try:
                User.objects.create_user(username=username, email=email, password=password)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AffiliateUserWithRegionAPIHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        zipcode = request.data.get('zipcode', None)
        if zipcode:
            region = get_object_or_404(Region, zipcode=zipcode)
            cohort = region.cohort

            cohort.members.add(request.user)
            response = {
                'cohort': cohort.name
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)