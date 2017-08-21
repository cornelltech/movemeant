from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Device
from .serializers import DeviceSerializer


class DeviceCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer
