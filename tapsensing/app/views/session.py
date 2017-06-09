from datetime import date

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

        response = {
            'exists': Session.objects.filter(date=today, user=user).exists()
        }

        return Response(response)
