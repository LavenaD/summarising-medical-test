import os

from medical_records.models import MedicalRecord
from .serializers import MedicalRecordSerializer, ProcessFileSerializer
from django.conf import settings
from rest_framework import viewsets
from medical_records.filters import MedicalRecordFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from medical_records.medicalRecordProcessor import MedicalRecordProcessor
import logging
import datetime

logger = logging.getLogger(__name__)


# from .serializers import MedicalRecordSerializer

#function based views
# @api_view(['GET', 'POST'])
# def MedicalRecordListView(request):
#     if request.method == 'GET':
#         queryset = MedicalRecord.objects.all()
#         serializer = MedicalRecordSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = MedicalRecordSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def MedicalRecordDetailsView(request, pk):
#     try:
#         medical_record = MedicalRecord.objects.get(pk=pk)
#     except MedicalRecord.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = MedicalRecordSerializer(medical_record)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         serializer = MedicalRecordSerializer(medical_record, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         medical_record.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#class Based Views
# class MedicalRecords(APIView):

#     def get(self, request):
#         queryset = MedicalRecord.objects.all()
#         serializer = MedicalRecordSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request):
#         serializer = MedicalRecordSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MedicalRecordsDetails(APIView):
#     def get(self, request, pk):
#         try:
#             medical_record = MedicalRecord.objects.get(pk=pk)
#         except MedicalRecord.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = MedicalRecordSerializer(medical_record)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def put(self, request, pk):
#         try:
#             medical_record = MedicalRecord.objects.get(pk=pk)
#         except MedicalRecord.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = MedicalRecordSerializer(medical_record, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self, request, pk):
#         try:
#             medical_record = MedicalRecord.objects.get(pk=pk)
#         except MedicalRecord.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         medical_record.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
 #mixins   
# class MedicalRecordsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = MedicalRecord.objects.all()
#     serializer_class = MedicalRecordSerializer

#     def get(self, request):
#         return self.list(request)
    
#     def post(self, request):
#         return self.create(request)

# class MedicalRecordsDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = MedicalRecord.objects.all()
#     serializer_class = MedicalRecordSerializer

#     def get(self, request, pk):
#         return self.retrieve(request, pk)
    
#     def put(self, request, pk):
#         return self.update(request, pk)
    
#     def delete(self, request, pk):
#         return self.destroy(request, pk)

#generic class based views
# class MedicalRecordsList(generics.ListCreateAPIView):
#     queryset = MedicalRecord.objects.all()
#     serializer_class = MedicalRecordSerializer
# class MedicalRecordsDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MedicalRecord.objects.all()
#     serializer_class = MedicalRecordSerializer

class MedicalRecordViewset(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    filterset_class = MedicalRecordFilter
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['patient_id', 'findings', 'labels', 'summary']
    ordering_fields = ['patient_id', 'findings', 'labels', 'summary']

class ProcessDirectoryFilesView(APIView):
    def post(self, request):
        serializer = ProcessFileSerializer(data=request.data)
        if serializer.is_valid():
            input_folder_path = serializer.validated_data.get('input_folder_path')
            max_rows_per_outputfile = serializer.validated_data.get('max_rows_per_outputfile')

        if not input_folder_path:
            return Response({"error": "Input folder path is required."}, status=status.HTTP_400_BAD_REQUEST)
        input_folder_path = os.path.join(settings.BASE_DIR, input_folder_path)
        input_folder_path = os.path.normpath(input_folder_path)
        # print(f"Processing files in directory: {input_folder_path}")
        rows_to_write = max_rows_per_outputfile if max_rows_per_outputfile is not None else 1000  # Default to 1000 if not provided

        try:
            medicalRecords =  MedicalRecordProcessor()
            response = medicalRecords.process_files(input_folder_path, rows_to_write)
            logger.info(f"File processing completed at {datetime.datetime.now()}: {response}")
            return Response({"message": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)