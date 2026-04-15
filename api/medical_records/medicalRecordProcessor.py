
import os

import medical_records.xmlReader as xml_reader
import medical_records.csvWriter as CsvWriter

class MedicalRecordProcessor():
    def __init__(self):
        self.data = []
        # self.previous_id = None
        # self.missing_id_files = []
        

    def process_files(self, input_folder_path, max_rows_per_outputfile=1000)-> str:
        print(f"Processing files in directory: {input_folder_path}")
        if not os.path.exists(input_folder_path):
            print(f"Input folder path '{input_folder_path}' does not exist.")
            return f"Input folder path '{input_folder_path}' does not exist."
        for file in os.listdir(input_folder_path):
            if file.endswith(".xml"):
                file_path = os.path.join(input_folder_path, file)
                reader = xml_reader.XmlReader()          
                data_dict = reader.read_file(file_path)
                
                # This code is used to store the missing file ids in the missing_id_files list. 
                # It checks if the current file's id is not equal to the previous file's id + 1 
                # which indicates that there is a missing file in the sequence. 
                # If a missing file is detected, its id is added to the missing_id_files list for later reference.
                if data_dict is not None:
                    self.data.append(data_dict) 
                    # if self.previous_id is None:
                    #     self.previous_id = data_dict.get("id").strip()
                    # else:
                    #     if int(data_dict.get("id").strip()) != int(self.previous_id) + 1:
                    #         self.missing_id_files.append(int(self.previous_id) + 1)    
                    # self.previous_id = data_dict.get("id").strip()

        return self.write_csv_file(max_rows_per_outputfile )
    def write_csv_file(self, max_rows_per_outputfile)-> str:
        csv_writer = CsvWriter.CsvWriter()
        return csv_writer.write_to_file(self.data, max_rows_per_outputfile)

# def main():


#     data = []
#     previous_id = None
#     missing_id_files = []

#     MODE = "VALIDATION"
#     FOLDER_PATH = TRAIN_FOLDER_PATH

#     if MODE == "VALIDATION":
#         FOLDER_PATH = VALIDATION_FOLDER_PATH
#     elif MODE == "TEST":
#         FOLDER_PATH = TEST_FOLDER_PATH


#     try:
#         for file in os.listdir(FOLDER_PATH):
#             if file.endswith(".xml"):
#                 file_path = os.path.join(FOLDER_PATH, file)
#                 reader = xml_reader.XmlReader()          
#                 data_dict = reader.read_file(file_path)
#                 if data_dict is not None:
#                     data.append(data_dict) 
#                     if previous_id is None:
#                         previous_id = data_dict.get("id").strip()
#                     else:
#                         if int(data_dict.get("id").strip()) != int(previous_id) + 1:
#                             missing_id_files.append(int(previous_id) + 1)    
#                     previous_id = data_dict.get("id").strip()

#         Write_csv_file(data, missing_id_files, 50)
#         # json_writer = jw.JsonWriter()
#         # json_writer.write_file(data)
#         # data_df = pd.DataFrame_from_dict(data, orient='index')
#         # data_df["tokenized_findings"] = data_df["findings"].apply(lambda x: word_tokenize(x))
#         # data_df["tokenized_impression"] = data_df["impression"].apply(lambda x: word_tokenize(x))
#         # data_df.to_csv("output.csv", index=False)
        
#     except Exception as e:
#         print(f"Error reading file {file_path}: {e}")




# def tokenize_text(text, nlp):
#     doc = nlp(text)
#     return [token.text for token in doc]

# if __name__ == "__main__":
#     main()
