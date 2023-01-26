from datetime import datetime
import csv
import chardet
import sys
import io
import pandas as pd
from collections import OrderedDict

def calculate_quality_measure_date(values):
    datetime_values = []
    for value in values:
        try:
            if isinstance(value, (float, int)):
                # Handle cases where value is a float or int
                value = str(value)
            datetime_value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            datetime_values.append(datetime_value)
        except (ValueError, TypeError):
            # value is not a valid datetime string, so we will skip it
            pass

    if len(datetime_values) > 0:
        oldest_date = min(datetime_values)
        newest_date = max(datetime_values)
        quality_measures = [(date - oldest_date).days / (newest_date - oldest_date).days * 5 for date in datetime_values]
        return quality_measures
    else:
        return []


def quality_measure(values, weight=1):
    lowest_value, highest_value = min(values), max(values)
    quality_measure = [(value - lowest_value) / (highest_value - lowest_value) * 5 * weight for value in values]
    return quality_measure


def calculate_quality_measure(file_name):
    # Read the CSV file
    df = pd.read_csv(file_name)

    # Calculate the average for each row
    df["quality_measure"] = df.mean(numeric_only=True, axis=1)

    # Save the DataFrame to a new CSV file
    df.to_csv("new_"+file_name, index=False)

    # Create a dictionary from the DataFrame
    qm = df.set_index("repository_url")["quality_measure"].to_dict()

    return qm


def read_csv_file(file_path):
    data = ""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        file.seek(0)
        csv_reader = csv.reader(file.read().decode(result['encoding']).splitlines())
        for row in csv_reader:
            data += ",".join(row) + "\n"
    return data


def extract_columns(csv_string: str, columns: list):
    # Create a DataFrame from the CSV string
    df = pd.read_csv(io.StringIO(csv_string))
    extracted_columns = {}
    for column in columns:
        extracted_columns[column] = df[column]
    return extracted_columns


def main():
    file_name = " ".join(sys.argv[1:])
    data = read_csv_file(file_name)

    columns = extract_columns(data, ["repository_name", "repository_url", "open_issue_count", "closed_issue_count", "open_closed_ratio", "commit_count", "original_codebase_size", "library_codebase_size", "library_to_original_ratio", "repository_type", "primary_language", "creation_date", "stargazer_count", "license_info", "latest_release"])

    # Quality Measure
    quality_measure_thresholds = OrderedDict()
    quality_measure_thresholds["repository_url"]  = columns["repository_url"] 
    quality_measure_thresholds["open_closed_ratio"] = quality_measure(columns["open_closed_ratio"])
    quality_measure_thresholds["commit_count"] = quality_measure(columns["commit_count"])
    quality_measure_thresholds["creation_date"] = calculate_quality_measure_date(columns["creation_date"])
    quality_measure_thresholds["stargazer_count"] = quality_measure(columns["stargazer_count"])
    quality_measure_thresholds["latest_release"] = calculate_quality_measure_date(columns["latest_release"])

    # Write to CSV
    df = pd.DataFrame(quality_measure_thresholds)
    df = df.rename(columns={0: 'repository_url'})
    df = df.rename(columns={1: 'open_closed_ratio'})
    df = df.rename(columns={2: 'commit_count'})
    df = df.rename(columns={3: 'creation_date'})
    df = df.rename(columns={4: 'stargazer_count'})
    df = df.rename(columns={5: 'latest_release'})
    df.to_csv('thresholds.csv', index=False)

    # Singular Quality Measures, Write to CSV    
    quality_measures = calculate_quality_measure("thresholds.csv")

    df = pd.DataFrame(quality_measures.items(), columns=['repository_url', 'quality_measure'])
    df.to_csv('quality_measures.csv', index=False)

    # Visualize Linear Regression
    # Ratio of Library Code : Open Closed Ratio
    # Ratio of Library Code : Stargazer Count
    # Ratio of Library Code : Commit Count
    # Ratio of Library Code : Creation Date
    # Ratio of Library Code : Latest Release
    # Ratio of Library Code : Average Quality Measure
    

main()