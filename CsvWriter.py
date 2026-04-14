import csv
import os


class CsvWriter():
    def write_to_file(self, data, output_file, rows_per_file=1000):
        
        file_exists = os.path.exists(output_file)
        row_num = 0
        
        with open(output_file, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            while row_num < rows_per_file and data:
                row = data.pop(row_num)
                if row is None:
                    break
                writer.writerow(row)
                row_num += 1
