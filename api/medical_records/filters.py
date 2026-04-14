import django_filters
from .models import MedicalRecord
class MedicalRecordFilter(django_filters.FilterSet):
    patient_id = django_filters.CharFilter(lookup_expr='icontains')
    findings = django_filters.CharFilter(lookup_expr='icontains')
    labels = django_filters.CharFilter(lookup_expr='icontains')
    summary = django_filters.CharFilter(lookup_expr='icontains')
    # id = django_filters.RangeFilter(field_name='id')

    class Meta:
        model = MedicalRecord
        fields = ['patient_id', 'findings', 'labels', 'summary', 'id']
