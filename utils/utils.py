import csv
import chardet
import pandas as pd
import sys
from datetime import datetime
import io

# Read a .csv file and return a string.
def read_csv_file(file_path):
    """
    Read a CSV file and return its contents as a string.

    Args:
        file_path (str): The path to the CSV file to read.

    Returns:
        str: The contents of the CSV file as a string, where each row is separated
            by a newline character and each value within a row is separated by a comma.
    """
    data = ""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        file.seek(0)
        csv_reader = csv.reader(file.read().decode(result['encoding']).splitlines())
        for row in csv_reader:
            data += ",".join(row) + "\n"

    return data

def extract_columns(dataset_file: str, columns: list):
    """
    Extract the specified columns from a CSV file and return them as a dictionary.

    Args:
        dataset_file (str): A string representing the contents of a CSV file.
        columns (list): A list of strings representing the names of the columns to extract.

    Returns:
        dict: A dictionary with the same keys as the `columns` argument, where each
            value is a list of tuples. Each tuple contains a unique identifier for the row
            (the 'repository_url' column in the original file) and the corresponding value
            for the specified column in that row.
    """
    # Create a DataFrame from the CSV string
    df = pd.read_csv(io.StringIO(dataset_file))

    extracted_columns = {}
    
    for column in columns:
        extracted_columns[column] = list(zip(df['repository_url'], df[column]))

    return extracted_columns

def print_columns(dataset_columns):
    """
    Print the names of the columns in a dataset.

    Args:
        dataset_columns (dict): A dictionary with column names as keys and lists of tuples as values.
            Each tuple contains a unique identifier for the row and the corresponding value for that
            column in that row.
    """
    for column, values in dataset_columns.items():
        print(column)


def print_values(dataset_columns, column_arg):
    """
    Print the values in the specified column of a dataset.

    Args:
        dataset_columns (dict): A dictionary with column names as keys and lists of tuples as values.
            Each tuple contains a unique identifier for the row and the corresponding value for that
            column in that row.
        column_arg (str): The name of the column to print the values of.
    """
    for column, values in dataset_columns.items():
        if column == column_arg:
            for value in values:
                print(f'{value[0]} : {value[1]}')

def convert_to_unix_timestamp(date_string):
    """
    Convert a date string in the format "%Y-%m-%dT%H:%M:%SZ" to a Unix timestamp.

    Args:
        date_string (str): A string representing a date in the format "%Y-%m-%dT%H:%M:%SZ".

    Returns:
        float: A Unix timestamp representing the same date and time as the input string.
    """
    date_format = "%Y-%m-%dT%H:%M:%SZ"

    datetime_object = datetime.strptime(date_string, date_format) 
    unix_timestamp = datetime_object.timestamp()
    
    return unix_timestamp