from rest_framework import serializers


def AllFieldSerializer(clazz):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = clazz
            fields = '__all__'
    return Serializer
