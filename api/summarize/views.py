from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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

logger = logging.getLogger(__name__)
# Create your views here.
class SummarizeFindingsView(APIView):

    def post(self, request):
        findings = request.data.get('findings')
        if not findings:
            return Response({"error": "Findings are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # load base model
        base_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small", token = True)
        logger.info(f"Base model loaded for summarization request at {datetime.datetime.now()}")

        # Hugging Face repo
        model_path = os.environ.get("HHUGGINGFACE_REPOSITORY", "LavenaD/medical-summarizer-peft")

        # attach LoRA adapter
        model = PeftModel.from_pretrained(base_model, model_path)

        # tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # print(datetime.datetime.now(), "Model and tokenizer loaded for job:", job_id)

        device = torch.device("cpu")
        model.to(device)

        prompted_batch = [
            "summarize medical report and return summary in no more than 2 sentences: " + str(findings)
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

        predictions = tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )
        
        # For demonstration purposes, we'll just return a dummy summary
        summary = f"Summary of findings: {predictions[0]}"  # Dummy summary
        
        return Response({"summary": summary}, status=status.HTTP_200_OK)
        