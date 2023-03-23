import csv
import chardet
import pandas as pd
import sys
import io

# Read a .csv file and return a string.
def read_csv_file(file_path):
    data = ""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        file.seek(0)
        csv_reader = csv.reader(file.read().decode(result['encoding']).splitlines())
        for row in csv_reader:
            data += ",".join(row) + "\n"

    return data

# Extract the Columns from the .csv file.
def extract_columns(csv_string: str, columns: list):
    # Create a DataFrame from the CSV string
    df = pd.read_csv(io.StringIO(csv_string))
    extracted_columns = {}
    for column in columns:
        extracted_columns[column] = df[column]

    return extracted_columns