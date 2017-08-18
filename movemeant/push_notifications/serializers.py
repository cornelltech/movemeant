from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'id', 'token', 'user', 'condition'
        )
        read_only = ('id', 'user', 'condition')

    def create(self, validated_data):
        if not hasattr(self.context['request'], 'user'):
            raise ValidationError('cannot proceed without logged-in user')

        user = getattr(self.context['request'], 'user')
        device = Device.objects.create(user=user, **validated_data)
        return device
