from datetime import date

from enum import Enum
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


class States(Enum):
    LAB_MODE = 'LAB_MODE'
    NOT_DONE_TODAY = 'NOT_DONE_TODAY'
    DONE_TODAY = 'DONE_TODAY'
    COMPLETED = 'COMPLETED'


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

        state = States.NOT_DONE_TODAY

        session_exists = Session.objects.filter(
            date=today,
            user=user,
            lab_mode=False
        ).exists()

        if session_exists:
            state = States.DONE_TODAY

        if self.check_sessions_completed(user):
            state = States.COMPLETED

        if hasattr(user, 'usersettings'):
            if user.usersettings.lab_mode:
                state = States.LAB_MODE

        response = {
            # This is from version 1
            'exists': False,
            # This is the new state var.
            'state': state.value
        }

        return Response(response)
