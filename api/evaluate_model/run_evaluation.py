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

def run_evaluation_job(job_id):
    logger.info(f"Starting evaluation job: {job_id}")
    # load base model
    base_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    logger.info(f"Base model loaded for job: {job_id} at {datetime.datetime.now()}")

    # Hugging Face repo
    model_path = config("HHUGGINGFACE_REPOSITORY", "LavenaD/medical-summarizer-peft")
    logger.info(f"Using model path: {model_path} for job: {job_id}")
    # attach LoRA adapter
    model = PeftModel.from_pretrained(base_model, model_path)
    logger.info(f"LoRA adapter attached for job: {job_id}")

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    logger.info(f"Tokenizer loaded for job: {job_id} at {datetime.datetime.now()}")
    # print(datetime.datetime.now(), "Model and tokenizer loaded for job:", job_id)

    device = torch.device("cpu")
    model.to(device)

    # print(datetime.datetime.now(), "Model moved to device for job:", job_id)

    # load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = config("EVALUATION_CSV", "output_validation_20260415071239.csv")
    csv_path = os.path.join(script_dir, "..", "output", file_name)
    logger.info(f"Loading evaluation data from: {csv_path}")
    test_df = pd.read_csv(csv_path)

    logger.info(f"Test data loaded for job: {job_id} at {datetime.datetime.now()}")

    inputs = test_df["findings"].tolist()
    references = test_df["labels"].tolist()

    # predict
    predictions = []

    batch_size = 8  # try 4, 8, or 16 depending on memory
    predictions = []

    model.eval()

    for start_idx in range(0, len(inputs), batch_size):
        end_idx = min(start_idx + batch_size, len(inputs))
        batch_texts = inputs[start_idx:end_idx]

        logger.info(
            f"Generating output for batch {start_idx}:{end_idx} in job {job_id} at {datetime.datetime.now()}"
        )

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

        logger.info(
            f"Decoded output for batch {start_idx}:{end_idx} in job {job_id} at {datetime.datetime.now()}"
        )

    logger.info(f"All predictions generated for job: {job_id} at {datetime.datetime.now()}")

    rouge = evaluate.load("rouge")

    results = rouge.compute(
        predictions=predictions,
        references=references
    )

    logger.info(f"Evaluation results for job {job_id} at {datetime.datetime.now()}: {results}")
