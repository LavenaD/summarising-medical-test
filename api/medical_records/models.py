from django.db import models

# Create your models here.
class MedicalRecord(models.Model):
    patient_id = models.CharField(max_length=100)
    findings = models.CharField(max_length=255)
    labels = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)

    def __str__(self):
        return self.patient_id
    