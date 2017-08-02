from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Session
from ..utils.viewset import CRUDViewSet
from ..utils.serializers import AllFieldSerializer


class SessionSerializer(AllFieldSerializer(Session)):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class SessionViewSet(CRUDViewSet(Session)):
    permissions = (IsAuthenticated,)
    serializer_class = SessionSerializer

    @list_route(methods=['get'], permissions=(IsAuthenticated,))
    def exists(self, request):
        today = date.today()
        user = request.user

        session_exists = Session.objects.filter(date=today, user=user).exists()
        # change exists for day if app is currently in lab mode.

        if hasattr(user, 'usersettings'):
            session_exists = False if request.user.usersettings.lab_mode else session_exists

        response = {
            'exists': session_exists
        }

        return Response(response)
