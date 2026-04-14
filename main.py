
import os

from nltk import data
import XmlReader as xml_reader
import CsvWriter
from nltk.tokenize import word_tokenize
import JsonWriter as jw
# import pandas as pd


def main():
    TRAIN_FOLDER_PATH = "data\\ecgen-radiology\\train"
    VALIDATION_FOLDER_PATH = "data\\ecgen-radiology\\validation"
    TEST_FOLDER_PATH = "data\\ecgen-radiology\\test"

    data = []
    previous_id = None
    missing_id_files = []

    MODE = "VALIDATION"
    FOLDER_PATH = TRAIN_FOLDER_PATH

    if MODE == "VALIDATION":
        FOLDER_PATH = VALIDATION_FOLDER_PATH
    elif MODE == "TEST":
        FOLDER_PATH = TEST_FOLDER_PATH


    try:
        for file in os.listdir(FOLDER_PATH):
            if file.endswith(".xml"):
                file_path = os.path.join(FOLDER_PATH, file)
                reader = xml_reader.XmlReader()          
                data_dict = reader.read_file(file_path)
                if data_dict is not None:
                    data.append(data_dict) 
                    if previous_id is None:
                        previous_id = data_dict.get("id").strip()
                    else:
                        if int(data_dict.get("id").strip()) != int(previous_id) + 1:
                            missing_id_files.append(int(previous_id) + 1)    
                    previous_id = data_dict.get("id").strip()

        Write_csv_file(data, missing_id_files, 50)
        # json_writer = jw.JsonWriter()
        # json_writer.write_file(data)
        # data_df = pd.DataFrame_from_dict(data, orient='index')
        # data_df["tokenized_findings"] = data_df["findings"].apply(lambda x: word_tokenize(x))
        # data_df["tokenized_impression"] = data_df["impression"].apply(lambda x: word_tokenize(x))
        # data_df.to_csv("output.csv", index=False)
        
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def Write_csv_file(data, missing_id_files, rows_per_file):
    try:
        # print("Writing to CSV... Missing IDs: {} (Total: {}) ".format(missing_id_files, len(data)))
        writer = CsvWriter.CsvWriter()
        writer.write_to_file(data, "output_600.csv", rows_per_file)
        return writer
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def tokenize_text(text, nlp):
    doc = nlp(text)
    return [token.text for token in doc]

if __name__ == "__main__":
    main()
