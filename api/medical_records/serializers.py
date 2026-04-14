from rest_framework import serializers
from medical_records.models import MedicalRecord
class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

class ProcessFileSerializer(serializers.Serializer):
    input_folder_path = serializers.CharField(max_length=255)
    max_rows_per_outputfile = serializers.IntegerField(default=1000)