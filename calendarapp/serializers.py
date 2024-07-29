from rest_framework import serializers


class ICSFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
