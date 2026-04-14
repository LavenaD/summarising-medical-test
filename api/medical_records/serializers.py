from rest_framework import serializers
from medical_records.models import MedicalRecord
class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'