from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
import threading
from .run_evaluation import run_evaluation_job
# Create your views here.
class EvaluateModelView(APIView):
    JOB_STORE = {}
    # simple in-memory store
    def post(self, request):
        try:
            job_id = str(uuid.uuid4())
            self.JOB_STORE[job_id] = {"status": "queued"}

            thread = threading.Thread(
                target=run_evaluation_job,
                args=(job_id,)
            )
            thread.start()

            return Response({
                "job_id": job_id,
                "status": "started"
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_status(self, request, job_id):
        job = self.JOB_STORE.get(job_id)

        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(job)
        # Here you would implement the logic to evaluate the model
        # For demonstration purposes, we'll just return a dummy evaluation result
        # evaluation_result = {
        #     "accuracy": 0.95,
        #     "precision": 0.92,
        #     "recall": 0.93,
        #     "f1_score": 0.925
        # }

        
        
        # return Response({"evaluation_result": evaluation_result}, status=status.HTTP_200_OK)
  