from datetime import date

from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Session
from ..utils.viewset import CRUDViewSet


class SessionViewSet(CRUDViewSet(Session)):
    permissions = (IsAuthenticated,)

    @list_route(methods=['post'], permissions=(IsAuthenticated,))
    def start(self, request):

        # check if trail exists for day and user
        today = date.today()
        session_exists_for_today = SessionViewSet.objects.filter(date=today, user=request.user).exists()

        # if it exists return the trail has already started
        if session_exists_for_today:
            response = Response(status=status.HTTP_412_PRECONDITION_FAILED)

        else:
            sesion = Session()
            sesion.date = today
            sesion.status = SessionViewSet.SITTING
            sesion.user = request.user
            sesion.save()

            response = Response()

        return response
