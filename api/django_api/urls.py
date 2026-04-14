from django.urls import path
from rest_framework.routers import DefaultRouter
from accounts import views as accounts_views
from medical_records import views as medical_records_views
from summarize import views as summarize_views
from evaluate import views as evaluate_views

# from .serializers import MedicalRecordSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
# router.register(r'medical_records', medical_records_views.MedicalRecordViewset, basename='medical-records')
router.register(r'accounts', accounts_views.UserCreateView, basename='accounts')

# API endpoints will return json response
urlpatterns = [
    #function based views
    # path('medical_records/', medical_records_views.MedicalRecordListView, name='medical-record-list'),
    # path('medical_records/<int:pk>/', medical_records_views.MedicalRecordDetailsView, name='medical-record-detail'),
    
    # Class Based Views
    # path('medical_records/', medical_records_views.MedicalRecords.as_view(), name='medical-record-list'),
    # path('medical_records/<int:pk>/', medical_records_views.MedicalRecordsDetails.as_view(), name='medical-record-detail'),
   
    #mixins and generics
    # path('medical_records/', medical_records_views.MedicalRecordsList.as_view(), name='medical-record-list'),
    # path('medical_records/<int:pk>/', medical_records_views.MedicalRecordsDetails.as_view(), name='medical-record-detail'),

    # path('medical_records/', medical_records_views.MedicalRecordsList.as_view(), name='medical-record-list'),
    # path('medical_records/<int:pk>/', medical_records_views.MedicalRecordsDetails.as_view(), name='medical-record-detail'),

    # path('', include(router.urls)),
    path('register/', accounts_views.UserCreateView.as_view(), name='user-create'),
    path('protected-view/', accounts_views.ProtectedView.as_view(), name='protected-view'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('medical_records/process/', medical_records_views.ProcessDirectoryFilesView.as_view(), name='process-medical-records'),  
    path('medical_records/', medical_records_views.MedicalRecordViewset.as_view({'get': 'list'}), name='medical-records'),
    path('summarize/', summarize_views.SummarizeFindingsView.as_view(), name='summarize-findings'),
    path('evaluate/', evaluate_views.EvaluateModelView.as_view(), name='evaluate-model'),
]