from django.contrib import admin
from .models import MedicalRecord
from evaluate_model.models import EvaluationJob

# Register your models here.
admin.site.register(MedicalRecord) 
admin.site.register(EvaluationJob) 