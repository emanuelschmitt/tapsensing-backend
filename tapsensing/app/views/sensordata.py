import logging

from django.contrib.auth.models import User
from rest_framework import permissions, serializers, status, parsers
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response

from ..models import SensorData
from ..utils.serializers import AllFieldSerializer

logger = logging.getLogger(__name__)


class SensorDataSerializer(AllFieldSerializer(SensorData)):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([parsers.JSONParser])
def sensor_data(request):

    serializer = SensorDataSerializer(data=request.data, many=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    data = serializer.validated_data.items()

    SensorData.objects.bulk_create(data, 50)

    response = {
        'count': len(serializer.validated_data)
    }

    return Response(response, status=status.HTTP_200_OK)
