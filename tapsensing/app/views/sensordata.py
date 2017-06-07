import logging

from rest_framework import permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import SensorData
from ..utils.serializers import AllFieldSerializer


logger = logging.getLogger(__name__)


class SensorDataSerializer(AllFieldSerializer(SensorData)):
    pass


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def sensor_data(request):

    try:
        sensordata = request.data.data
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = SensorDataSerializer(data=sensordata, many=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.error_messages)

    serializer.save()
    logger.info("sensor_data_endpoint called.")

    return Response(status=status.HTTP_200_OK)
