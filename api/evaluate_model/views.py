from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
import threading
import pandas as pd
import torch
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
import os
import datetime
from decouple import config
import logging
from evaluate_model.serializers import EvaluateFileSerializer
from evaluate_model.models import EvaluationJob

logger = logging.getLogger(__name__)

# Create your views here.
class EvaluateModelView(APIView):

    @classmethod
    def check_job_exists(self, job_id):
        return EvaluationJob.objects.filter(job_id=job_id).exists()
    
    @classmethod
    def update_job_status(self, job_id, status, progress=None, results=None):
        job = EvaluationJob.objects.filter(job_id=job_id).first()
        if job:
            job.status = status
            if progress is not None:
                job.progress = progress
            if results is not None:
                job.result = f"{results}"
                print(f"Updating job {job_id} with results: {results}")
            job.save()

        

    @classmethod
    def run_evaluation_job(self, job_id, input_file_name):
        logger.info(f"Starting evaluation job: {job_id} at {datetime.datetime.now()}")
        # load base model
        base_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small",
        token=config("HUGGINGFACEHUB_API_TOKEN"))

        # Hugging Face repo
        model_path = config("HHUGGINGFACE_REPOSITORY", "LavenaD/medicalSummarizerPeft")

        # attach LoRA adapter
        model = PeftModel.from_pretrained(base_model, model_path)
        logger.info(f"LoRA adapter attached for job: {job_id} at {datetime.datetime.now()}")

        # tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        logger.info(f"Tokenizer loaded for job: {job_id} at {datetime.datetime.now()}")

        # print(datetime.datetime.now(), "Model and tokenizer loaded for job:", job_id)

        device = torch.device("cpu")
        model.to(device)

        # print(datetime.datetime.now(), "Model moved to device for job:", job_id)

        # load data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "..", "output", input_file_name)
        logger.info(f"Loading evaluation data from: {csv_path}")
        test_df = pd.read_csv(csv_path)
        logger.info(f"Test data loaded for job: {job_id} at {datetime.datetime.now()}")


        inputs = test_df["findings"].tolist()
        references = test_df["labels"].tolist()

        batch_size = 8  # try 4, 8, or 16 depending on memory
        predictions = []

        model.eval()

        complete_job = len(inputs) + 5

        job = EvaluationJob.objects.filter(job_id=job_id).first()

        for start_idx in range(0, len(inputs), batch_size):
            end_idx = min(start_idx + batch_size, len(inputs))
            batch_texts = inputs[start_idx:end_idx]

            progress = 96 if int((end_idx / complete_job) * 100) > 96 else int((end_idx / complete_job) * 100)

            EvaluateModelView.update_job_status(job_id, f"running - Generating output for batch {start_idx}:{end_idx}", progress)

            prompted_batch = [
                "summarize medical report and return summary in no more than 2 sentences: " + str(text)
                for text in batch_texts
            ]
            logger.info(
                f"Generating output for batch {start_idx}:{end_idx} in job {job_id} at {datetime.datetime.now()}"
            )

            tokens = tokenizer(
                prompted_batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=256
            ).to(device)

            with torch.no_grad():
                outputs = model.generate(
                    **tokens,
                    max_length=64,
                    num_beams=4
                )

            batch_predictions = tokenizer.batch_decode(
                outputs,
                skip_special_tokens=True
            )

            logger.info(
                f"Decoded output for batch {start_idx}:{end_idx} in job {job_id} at {datetime.datetime.now()}"
            )

            predictions.extend(batch_predictions)


        logger.info(f"All predictions generated for job: {job_id} at {datetime.datetime.now()}")
        print(f"All predictions generated for job: {job_id} at {datetime.datetime.now()}")

        progress = 96 if int((end_idx / complete_job) * 100) > 96 else int((end_idx / complete_job) * 100)

        EvaluateModelView.update_job_status(job_id, f"running - All predictions generated. Calculating ROUGE scores..", progress)

        rouge = evaluate.load("rouge")

        results = rouge.compute(
            predictions=predictions,
            references=references
        )

        EvaluateModelView.update_job_status(job_id, f"Completed - Evaluation finished with ROUGE scores calculated", 100, results)

        logger.info(f"Evaluation results for job {job_id} at {datetime.datetime.now()}: {results}")

class StartEvaluationView(APIView):
    def post(self, request):
        try:
            job_id = str(uuid.uuid4())

            serializer = EvaluateFileSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "errors": serializer.errors,
                        "received_data": request.data,
                        "content_type": request.content_type,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            input_file_name = serializer.validated_data.get('input_file_name')

            if EvaluateModelView.check_job_exists(job_id):
                return Response(
                    {"error": "Job ID collision, please try again"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )            


            EvaluationJob.objects.create(job_id=job_id, status="queued")

            thread = threading.Thread(
                target= EvaluateModelView.run_evaluation_job,
                args=(job_id,input_file_name,)
            )
            thread.start()

            return Response({
                "job_id": str(job_id),
                "status": "started"
            })
        except Exception as e:
            logger.error(f"Error starting evaluation job at {datetime.datetime.now()}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EvaluationStatusView(APIView):   
    def get(self, request, job_id):
        try:
            job = EvaluationJob.objects.filter(job_id=job_id).first()

            logger.info(f"Status check for job {job_id} at {datetime.datetime.now()}: {job}")

            if not job:
                return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "job_id": str(job.job_id),
                "status": job.status,
                "result": job.result,
                "progress": job.progress,
                "created_at": job.created_at.isoformat(),
            })
        except Exception as e:
            logger.error(f"Error checking status for job {job_id} at {datetime.datetime.now()}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
