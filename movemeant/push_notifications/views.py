from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Device
from .serializers import DeviceSerializer


class DeviceCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

