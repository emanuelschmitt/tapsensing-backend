import logging

from django.contrib.auth.models import User
from rest_framework import permissions, serializers, status, parsers
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response

from ..models import PreTestSurvey
from ..utils.serializers import AllFieldSerializer

logger = logging.getLogger(__name__)


class PreTestSurveySerializer(AllFieldSerializer(PreTestSurvey)):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@parser_classes([parsers.JSONParser])
def pretest_survey(request):

    serializer = PreTestSurvey(data=request.data, many=True)

    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    serializer.save()

    response = {
        'msg': 'success'
    }

    return Response(response, status=status.HTTP_200_OK)
