import pandas as pd
import torch
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
import os
import datetime

def run_evaluation_job(job_id):
    print(datetime.datetime.now(), "Starting evaluation job:", job_id)
    # load base model
    base_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

    # Hugging Face repo
    model_path = os.environ.get("HHUGGINGFACE_REPOSITORY", "LavenaD/medical-summarizer-peft")
    # model_path = "LavenaD/medical-summarizer-peft"
    # model_path = f"hf://{model_path}"


    # attach LoRA adapter
    model = PeftModel.from_pretrained(base_model, model_path)

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    print(datetime.datetime.now(), "Model and tokenizer loaded for job:", job_id)

    device = torch.device("cpu")
    model.to(device)

    print(datetime.datetime.now(), "Model moved to device for job:", job_id)

    # load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "..", "output", "output_validation_20260415071239.csv")
    test_df = pd.read_csv(csv_path)

    print(datetime.datetime.now(), "Test data loaded for job:", job_id)

    inputs = test_df["findings"].tolist()
    references = test_df["labels"].tolist()

    # predict
    predictions = []

    for text in inputs:
        print(datetime.datetime.now(), f"Generating output for{text} in job {job_id}")

        text = "summarize medical report and return summary in no more than 2 sentences: " + text

        tokens = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256
        ).to(device)

        output = model.generate(
            **tokens,
            max_length=64,
            num_beams=4
        )

        print(datetime.datetime.now(), f"Decoded output for{text} in job {job_id}")

        pred = tokenizer.decode(
            output[0],
            skip_special_tokens=True
        )

        predictions.append(pred)

    print(datetime.datetime.now(), "All predictions generated for job:", job_id)
    # rouge
    rouge = evaluate.load("rouge")

    results = rouge.compute(
        predictions=predictions,
        references=references
    )

    print(results)
