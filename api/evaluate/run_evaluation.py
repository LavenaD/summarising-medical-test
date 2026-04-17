import pandas as pd
import torch
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel

def run_evaluation_job(job_id):
    model_path = r"api\\django_api\\ai_model"
    print(model_path)

    # load base model
    base_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

    # attach LoRA adapter
    model = PeftModel.from_pretrained(base_model, model_path)

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    device = torch.device("cpu")
    model.to(device)

    # load data
    test_df = pd.read_csv("api\\output\\output_validation_20260415071239.csv")

    inputs = test_df["findings"].tolist()
    references = test_df["labels"].tolist()

    # predict
    predictions = []

    for text in inputs:

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

        pred = tokenizer.decode(
            output[0],
            skip_special_tokens=True
        )

        predictions.append(pred)

    print(predictions)
    # rouge
    rouge = evaluate.load("rouge")

    results = rouge.compute(
        predictions=predictions,
        references=references
    )

    print(results)
