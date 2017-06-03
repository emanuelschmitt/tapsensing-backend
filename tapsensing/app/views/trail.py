from datetime import date

from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Trail
from ..utils.viewset import CRUDViewSet


class TrailViewset(CRUDViewSet(Trail)):
    permissions = (IsAuthenticated,)

    @list_route(methods=['post'], permissions=(IsAuthenticated,))
    def start(self, request):

        # check if trail exists for day and user
        today = date.today()
        trail_exists_for_today = Trail.objects.filter(date=today, user=request.user).exists()

        # if it exists return the trail has already started
        if trail_exists_for_today:
            response = Response(status=status.HTTP_412_PRECONDITION_FAILED)

        else:
            trail = Trail()
            trail.date = today
            trail.status = Trail.STATUS_STARTED
            trail.user = request.user
            trail.save()

            response = Response(status=status.HTTP_200_OK)

        return response
