from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=serializer.errors)

    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)

    response = {
        'token': token.key,
        'user_id': user.id,
    }

    return Response(response)
