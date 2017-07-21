import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework import permissions, status, parsers
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def trial_settings(request):

    try:

        trial_setting = settings.TRIAL_SETTINGS
        shapes = trial_setting['SHAPES']
        repeats = trial_setting['REPEATS']

    except KeyError:
        raise ImproperlyConfigured('Trail Settings are not properly set.')

    response = {
        'shapes': shapes,
        'repeats': repeats
    }

    return Response(response, status=status.HTTP_200_OK)
