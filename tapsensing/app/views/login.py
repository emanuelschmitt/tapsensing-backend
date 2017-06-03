from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


class LoginTokenView(APIView):
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_401_UNAUTHORIZED, data=serializer.errors)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        response = {
            'token': token.key,
            'user_id': user.id,
        }

        return Response(response)
