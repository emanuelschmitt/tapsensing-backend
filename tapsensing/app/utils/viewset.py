from rest_framework import viewsets
from .serializers import AllFieldSerializer


def CRUDViewSet(clazz):
    class ViewSet(viewsets.ModelViewSet):
        queryset = clazz.objects.all()
        serializer_class = AllFieldSerializer(clazz)

    return ViewSet

