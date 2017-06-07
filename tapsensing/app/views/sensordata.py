import logging

from rest_framework import permissions, serializers, status, parsers
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response

from ..models import SensorData
from ..utils.serializers import AllFieldSerializer

logger = logging.getLogger(__name__)


class SensorDataListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [SensorData(**item) for item in validated_data]
        return SensorData.objects.bulk_create(books)


class SensorDataSerializer(serializers.Serializer):
    class Meta:
        model = SensorData
        fields = '__all__'
        list_serializer_class = SensorDataListSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([parsers.JSONParser])
def sensor_data(request):
    logger.info(request.data)

    serializer = SensorDataListSerializer(data=request.data, many=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    serializer.save()
    logger.info("sensor_data_endpoint called.")

    return Response(status=status.HTTP_200_OK)
