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

    def perform_create(self, serializer):
        serializer.save(lab_mode=self.request.user.usersettings.lab_mode)

    @staticmethod
    def check_sessions_completed(user):
        non_lab_session_count = Session.objects.filter(user=user, lab_mode=False).count()
        return non_lab_session_count == settings.AMOUNT_NON_LAB_SESSIONS

    @list_route(methods=['get'], permissions=(IsAuthenticated,))
    def exists(self, request):
        today = date.today()
        user = request.user

        session_exists = Session.objects.filter(
            date=today,
            user=user,
            lab_mode=False
        ).exists()
        # change exists for day if app is currently in lab mode.

        if hasattr(user, 'usersettings'):
            session_exists = False if request.user.usersettings.lab_mode else session_exists

        completed = self.check_sessions_completed(user)

        response = {
            'exists': session_exists,
            'completed': completed
        }

        return Response(response)
