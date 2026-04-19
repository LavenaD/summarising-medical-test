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

# Create your views here.
class EvaluateModelView(APIView):
    JOB_STORE = {}

    @classmethod
    def check_job_exists(self, job_id):
        return job_id in self.JOB_STORE

    @classmethod
    def run_evaluation_job(self, job_id):
        print(datetime.datetime.now(), "Starting evaluation job:", job_id)
        # load base model
        base_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small",
        tokem=True)

        # Hugging Face repo
        model_path = config("HHUGGINGFACE_REPOSITORY", "LavenaD/medical-summarizer-peft")

        # attach LoRA adapter
        model = PeftModel.from_pretrained(base_model, model_path)

        # tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # print(datetime.datetime.now(), "Model and tokenizer loaded for job:", job_id)

        device = torch.device("cpu")
        model.to(device)

        # print(datetime.datetime.now(), "Model moved to device for job:", job_id)

        # load data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = config("EVALUATION_CSV", "output_validation_20260415071239.csv")
        csv_path = os.path.join(script_dir, "..", "output", file_name)
        print(f"Loading evaluation data from: {csv_path}")
        test_df = pd.read_csv(csv_path)

        print(datetime.datetime.now(), "Test data loaded for job:", job_id)

        inputs = test_df["findings"].tolist()
        references = test_df["labels"].tolist()

        batch_size = 8  # try 4, 8, or 16 depending on memory
        predictions = []

        model.eval()

        complete_job = len(inputs) + 5

        for start_idx in range(0, len(inputs), batch_size):
            end_idx = min(start_idx + batch_size, len(inputs))
            batch_texts = inputs[start_idx:end_idx]

            progress = 96 if int((end_idx / complete_job) * 100) > 96 else int((end_idx / complete_job) * 100)

            EvaluateModelView.JOB_STORE[job_id]= {
                "status": f"running - Generating output for batch {start_idx}:{end_idx}",
                "progress": progress
            }

            prompted_batch = [
                "summarize medical report and return summary in no more than 2 sentences: " + str(text)
                for text in batch_texts
            ]

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

            predictions.extend(batch_predictions)

            print(
                datetime.datetime.now(),
                f"Decoded output for batch {start_idx}:{end_idx} in job {job_id}"
            )

        print(datetime.datetime.now(), f"All predictions generated for job: {job_id}")

        progress = 96 if int((end_idx / complete_job) * 100) > 96 else int((end_idx / complete_job) * 100)

        EvaluateModelView.JOB_STORE[job_id]= {
            "status": f"running - All predictions generated. Calculating ROUGE scores..",
            "progress": progress
        }

        rouge = evaluate.load("rouge")

        results = rouge.compute(
            predictions=predictions,
            references=references
        )

        EvaluateModelView.JOB_STORE[job_id]= {
            "status": f"Completed - Evaluation finished with ROUGE scores calculated",
            "progress": 100,
            "results": results
        }

        print(results)

class StartEvaluationView(APIView):
    def post(self, request):
        try:
            job_id = str(uuid.uuid4())

            if EvaluateModelView.check_job_exists(job_id):
                return Response(
                    {"error": "Job ID collision, please try again"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )            


            EvaluateModelView.JOB_STORE[job_id] = {"status": "queued", "progress": 0}

            thread = threading.Thread(
                target= EvaluateModelView.run_evaluation_job,
                args=(job_id,)
            )
            thread.start()

            return Response({
                "job_id": job_id,
                "status": "started"
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EvaluationStatusView(APIView):   
    def get(self, request, job_id):
        job = EvaluateModelView.JOB_STORE.get(job_id)

        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(job)
    
    
