import logging
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from tapsensing.app.models import SensorData
from tapsensing.app.utils.serializers import AllFieldSerializer


logger = logging.getLogger(__name__)


class SensorDataSerializer(AllFieldSerializer(SensorData)):
    pass


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def sensor_data(request):

    logger.debug(request.data)
    user = request.user

    return Response()