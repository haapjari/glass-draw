from datetime import datetime
import csv
import chardet
import sys
import io
import pandas as pd
from collections import OrderedDict
import numpy
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import pearsonr


# Calculate the Quality Measure for the Columns, which have Date.
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


# Calculate the Quality Measure.
def quality_measure(values):
    lowest_value, highest_value = min(values), max(values)
    quality_measure = [(value - lowest_value) / (highest_value - lowest_value) * 5 for value in values]
    return quality_measure


# Calculate the Quality Measure for the each row in the .csv file.
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


# Calculate and draw a plot for the Library to Original Ratio and Quality Measure.
def plot_library_ratio_to_qm():
    quality_measures = calculate_quality_measure("thresholds.csv")
    quality_measures_df = pd.DataFrame(quality_measures.items(), columns=['repository_url', 'quality_measure'])
    quality_measures_df.to_csv('quality_measures.csv', index=False)
    original_dataset_df = pd.read_csv("dataset.csv")

    # Key - Value (URL, (Library to Original Ratio, Quality Measure))
    ratio_to_quality_measure = {}
    for index, row in original_dataset_df.iterrows():
        if row['repository_url'] == quality_measures_df.iloc[index]['repository_url']:
            ratio_to_quality_measure.update({row['repository_url']: (row['library_to_original_ratio'], quality_measures_df.iloc[index]['quality_measure'])})

    # Calculate Linear Regression between Library to Original Ratio and Quality Measure
    x = []
    y = []
    for key, value in ratio_to_quality_measure.items():
        x.append(value[0])
        y.append(value[1])
    
    corr, _ = pearsonr(x, y) 
    corr = round(corr, 5)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.1, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library Code : Original Code Ratio')
    plt.ylabel('Quality Measure')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.legend(["Pearson's Correlation: " + str(corr)])

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    # Limiting the x -axis to make the plot more readable.
    plt.xlim(-100, 5000) 
    plt.ylim(0, 5)
    plt.show()


# Calculate and draw a plot for the Library to Original Ratio and Quality Measure.
def plot_to_releases():
    dataset_df = pd.read_csv("dataset.csv")
    thresholds_df = pd.read_csv("thresholds.csv")

    # Key - Value (URL, (Library to Original Ratio, Quality Measure))
    list = {}
    for index, row in dataset_df.iterrows():
        if row['repository_url'] == thresholds_df.iloc[index]['repository_url']:
            list.update({row['repository_url']: (row['library_to_original_ratio'], thresholds_df.iloc[index]['latest_release'])})

    # Calculate Linear Regression between Library to Original Ratio and Quality Measure
    x = []
    y = []
    for key, value in list.items():
        x.append(value[0])
        y.append(value[1])
    
    corr, _ = pearsonr(x, y) 
    corr = round(corr, 5)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.1, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library Code : Original Code Ratio')
    plt.ylabel('Latest Release')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.legend(["Pearson's Correlation: " + str(corr)])

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    # Limiting the x -axis to make the plot more readable.
    plt.xlim(-100, 5000) 
    plt.ylim(0, 5)
    plt.show()


# Calculate and draw a plot for the Library to Original Ratio and Quality Measure.
def plot_to_creation_date():
    dataset_df = pd.read_csv("dataset.csv")
    thresholds_df = pd.read_csv("thresholds.csv")

    # Key - Value (URL, (Library to Original Ratio, Quality Measure))
    list = {}
    for index, row in dataset_df.iterrows():
        if row['repository_url'] == thresholds_df.iloc[index]['repository_url']:
            list.update({row['repository_url']: (row['library_to_original_ratio'], thresholds_df.iloc[index]['creation_date'])})

    x = []
    y = []
    for key, value in list.items():
        x.append(value[0])
        y.append(value[1])
    
    corr, _ = pearsonr(x, y) 
    corr = round(corr, 5)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.1, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library Code : Original Code Ratio')
    plt.ylabel('Creation Dates')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.legend(["Pearson's Correlation: " + str(corr)])

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    # Limiting the x -axis to make the plot more readable.
    plt.xlim(-100, 5000) 
    plt.ylim(0, 5)
    plt.show()


# Calculate and draw a plot for the Library to Original Ratio and Open to Closed Ratio.
def plot_library_ratio_to_issues(data):
    columns = extract_columns(data, ["open_closed_ratio", "library_to_original_ratio"])

    # Calculate Linear Regression between Library to Original Ratio and Quality Measure
    x = []
    y = []

    for value in columns["library_to_original_ratio"]:
       x.append(value)

    for value in columns["open_closed_ratio"]:
       y.append(value) 

    corr, _ = pearsonr(x, y) 
    corr = round(corr, 5)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.05, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library Code : Original Code Ratio')
    plt.ylabel('Open Issues : Closed Issues Ratio')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.legend(["Pearson's Correlation: " + str(corr)])

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    # Limiting the x -axis to make the plot more readable.
    plt.xlim(-100, 5000) 
    plt.ylim(0, 5)
    plt.show()


# Calculate and Draw a Plot between Library to Original Ratio and Stargazer Count.
def plot_to_stars(data):
    columns = extract_columns(data, ["library_to_original_ratio", "stargazer_count"])

    x = []
    y = []

    for value in columns["library_to_original_ratio"]:
       x.append(value)

    for value in columns["stargazer_count"]:
       y.append(value) 

    corr, _ = pearsonr(x, y) 
    corr = round(corr, 5)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.05, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library Code : Original Code Ratio')
    plt.ylabel('Stargazer Count')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.legend(["Pearson's Correlation: " + str(corr)])

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    # Limiting the x -axis to make the plot more readable.
    plt.xlim(-50, 5000) 
    plt.ylim(-50, 10000)
    plt.show() 


# Calculate and Draw a Plot between Library to Original Ratio and Commit Count.
def plot_to_commits(data):
    columns = extract_columns(data, ["library_to_original_ratio", "commit_count"])

    x = []
    y = []

    for value in columns["library_to_original_ratio"]:
       x.append(value)

    for value in columns["commit_count"]:
       y.append(value) 

    corr, _ = pearsonr(x, y) 
    corr = round(corr, 5)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.05, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library Code : Original Code Ratio')
    plt.ylabel('Commit Count')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.legend(["Pearson's Correlation: " + str(corr)])

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    # Limiting the x -axis to make the plot more readable.
    plt.xlim(-50, 5000) 
    plt.ylim(-50, 5000)
    plt.show() 


# Generates Quality Measure Thresholds for each Repository.
def generate_thresholds(data):
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


def main():
    file_name = " ".join(sys.argv[1:])
    data = read_csv_file(file_name)

    # Visualize Linear Regression

    # Ratio of Library Code : Open Closed Ratio
    # Ratio of Library Code : Stargazer Count
    # Ratio of Library Code : Commit Count
    # Ratio of Library Code : Creation Date
    # Ratio of Library Code : Latest Release
    # Ratio of Library Code : Average Quality Measure

    generate_thresholds(data)
    plot_library_ratio_to_qm() 
    plot_library_ratio_to_issues(data)
    plot_to_stars(data)
    plot_to_commits(data)
    plot_to_creation_date()
    plot_to_releases()


if __name__ == "__main__": 
    main()