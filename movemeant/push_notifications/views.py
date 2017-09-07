from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Device


class DeviceCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        device_token = request.data.get('device', None)

        if device_token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        obj, created = Device.objects.get_or_create(
            user=user,
            token=device_token
        )

        return Response(status=status.HTTP_200_OK)
