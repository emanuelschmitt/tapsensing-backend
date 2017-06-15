import logging

from push_notifications.models import APNSDevice

from rest_framework import status, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class APNSTokenSerializer(serializers.Serializer):
    device_token = serializers.CharField(max_length=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def apns_register(request):
    serializers = APNSTokenSerializer(data=request.data)
    if not serializers.is_valid():
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    device_token = serializers.validated_data["device_token"]
    device, created = APNSDevice.objects.get_or_create(
        user=request.user
    )
    device.registration_id = device_token
    device.save()

    logger.info("Device registered for user %d with token %s".format(request.user.id, device_token))

    return Response({"msg": "success"})
