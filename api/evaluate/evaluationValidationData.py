import pandas as pd
import torch
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# load model
model_path = "/content/medical_model/final-artifacts-g5/medical_summarizer_model_g5"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

device = torch.device("cpu")
model.to(device)

# load data
test_df = pd.read_csv("/content/sample_data/output_validation_20260415071239.csv")

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