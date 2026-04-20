from rest_framework import serializers


class EvaluateFileSerializer(serializers.Serializer):
    input_file_name = serializers.CharField(max_length=255)