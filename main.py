from datetime import datetime
import csv
import chardet
import sys

def calculate_quality_measure_date(values):
    # convert all date strings to datetime objects
    datetime_values = [datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ') for value in values]
    # Find the oldest date in the list
    oldest_date = min(datetime_values)
    # Find the newest date in the list
    newest_date = max(datetime_values)
    # Count how many values in the list are older than newest_date
    below_newest_count = len([value for value in datetime_values if value < newest_date])
    # Calculate the quality measure by dividing the count of older than newest values by the length of the list
    quality_measure = below_newest_count / len(values) * 5
    # return the quality measure
    return quality_measure

def calculate_quality_measure(values):
    # Find the lowest value in the list
    lowest_value = min(values)

    # Find the highest value in the list
    highest_value = max(values)
    
    # Calculate the middle point between the lowest and highest value
    middle_point = (lowest_value + highest_value) / 2
    
    # Count how many values in the list are less than middle_point
    below_middle_count = len([value for value in values if value < middle_point])
    
    # Calculate the quality measure by dividing the count of below middle values by the length of the list
    quality_measure = below_middle_count / len(values) * 5
    
    # return the quality measure
    return quality_measure


def read_csv_file(file_path):
    data = ""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        file.seek(0)
        csv_reader = csv.reader(file.read().decode(result['encoding']).splitlines())
        for row in csv_reader:
            data += ",".join(row) + "\n"
    return data

def main():
    file_name = " ".join(sys.argv[1:])

    data = read_csv_file(file_name)
    print(data)

main()