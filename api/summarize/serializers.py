from rest_framework import serializers
class SummarizeFindingsSerializer(serializers.Serializer):
    findings = serializers.CharField(max_length=255, required=True)