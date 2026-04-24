import uuid

from django.db import models

# Create your models here.
class EvaluationJob(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, default="pending")
    result = models.JSONField(null=True, blank=True)
    rouge1 = models.FloatField(null=True, blank=True)
    rouge2 = models.FloatField(null=True, blank=True)
    rougeL = models.FloatField(null=True, blank=True)
    rougeLsum = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return str(self.job_id)