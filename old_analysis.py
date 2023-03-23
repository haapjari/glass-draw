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

# Set the Matplotlib Backend to Agg, so that the plots can be saved to a file.
mpl.use('agg')

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


# This function takes in a list of "values" as input and calculates a "quality measure" for each value in the list. 
# The quality measure is calculated as a value between 0 and 5, where 0 is the lowest value and 5 is the highest value. 
# The function returns a list of the quality measures for each input value.
def quality_measure(values):
    # Find the lowest and highest values in the input list
    lowest_value, highest_value = min(values), max(values)
    
    # Calculate the quality measure for each value in the input list
    quality_measure = [(value - lowest_value) / (highest_value - lowest_value) * 5 for value in values]
    
    # Return the list of quality measures
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








# Calculate and draw a plot for the Library to Original Ratio and Quality Measure.
def plot_library_ratio_to_qm():
    data = pd.read_csv("2023-03-21_normalized.csv")

    # Calculate the mean for each specified column
    mean_columns = ['open_closed_ratio', 'commit_count', 'creation_date', 'stargazer_count', 'latest_release']
    means = data[mean_columns].mean()

    # Save the means to a dictionary with the repository_url as a key
    quality_measure_dict = {}
    library_ratio_dict = {}
    for index, row in data.iterrows():
        repository_url = row['repository_url']

        mean_values = row[mean_columns].mean()
        quality_measure_dict[repository_url] = mean_values

        # Store the library_to_original_ratio value in the library_ratio_dict
        library_ratio = row['library_to_original_ratio']
        library_ratio_dict[repository_url] = library_ratio

    x = []  # Store library_to_original_ratio values
    y = []  # Store quality_measure values

    # Iterate through the keys in the library_ratio_dict
    for repository_url, library_ratio in library_ratio_dict.items():
    # Check if the repository_url exists in the mean_dict
        if repository_url in quality_measure_dict:
            quality_measure = quality_measure_dict[repository_url]
        
            x.append(library_ratio)
            y.append(quality_measure)
   
    correlation_coefficient, p_value = pearsonr(x, y) 
    correlation_coefficient = round(correlation_coefficient, 8)
    p_value = round(p_value, 8)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.1, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library to Original Code Ratio')
    plt.ylabel('Quality Measure')
    plt.autoscale(enable=True, axis='both', tight=None)

    legend_coefficient = plt.legend(["r = " + str(correlation_coefficient)], loc='upper right', bbox_to_anchor=(1.0, 1.0))
    legend_coefficient.set_title("Correlation Coefficient")
    legend_coefficient.get_title().set_fontsize('small')
    legend_coefficient.get_title().set_fontweight('bold')
    
    legend_p = plt.legend(["p = " + str(p_value)], loc='upper right', bbox_to_anchor=(1.0, 0.85))
    legend_p.set_title("Probability Value")
    legend_p.get_title().set_fontsize('small')
    legend_p.get_title().set_fontweight('bold')

    plt.gca().add_artist(legend_coefficient)
    plt.gca().add_artist(legend_p)

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    # Limiting the x -axis to make the plot more readable.
    plt.xlim(0, 5) 
    plt.ylim(0, 5)
    # plt.show()
    plt.savefig('library_ratio_to_qm.png', dpi=300, bbox_inches='tight', pad_inches=0.1)


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
    
    coefficient, pvalue = pearsonr(x, y) 
    coefficient = round(coefficient, 8)
    pvalue = round(pvalue, 8)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.1, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library to Original Code Ratio')
    plt.ylabel('Latest Release')
    plt.autoscale(enable=True, axis='both', tight=None)

    legend_coefficient = plt.legend(["r = " + str(coefficient)], loc='lower right', bbox_to_anchor=(1.0, 0.15))
    legend_coefficient.set_title("Correlation Coefficient")
    legend_coefficient.get_title().set_fontsize('small')
    legend_coefficient.get_title().set_fontweight('bold')
    
    legend_p = plt.legend(["p = " + str(pvalue)], loc='lower right', bbox_to_anchor=(1.0, 0.0))
    legend_p.set_title("Probability Value")
    legend_p.get_title().set_fontsize('small')
    legend_p.get_title().set_fontweight('bold')

    plt.gca().add_artist(legend_coefficient)
    plt.gca().add_artist(legend_p)

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
    
    coefficient, pvalue = pearsonr(x, y) 
    coefficient = round(coefficient, 8)
    pvalue = round(pvalue, 8)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.1, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library to Original Code Ratio')
    plt.ylabel('Creation Dates')
    plt.autoscale(enable=True, axis='both', tight=None)
    
    legend_coefficient = plt.legend(["r = " + str(coefficient)], loc='lower right', bbox_to_anchor=(1, 0.15))
    legend_coefficient.set_title("Correlation Coefficient")
    legend_coefficient.get_title().set_fontsize('small')
    legend_coefficient.get_title().set_fontweight('bold')
    
    legend_p = plt.legend(["p = " + str(pvalue)], loc='lower right', bbox_to_anchor=(1, 0.0))
    legend_p.set_title("Probability Value")
    legend_p.get_title().set_fontsize('small')
    legend_p.get_title().set_fontweight('bold')

    plt.gca().add_artist(legend_coefficient)
    plt.gca().add_artist(legend_p)

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

    coefficient, pvalue = pearsonr(x, y) 
    coefficient = round(coefficient, 8)
    pvalue = round(pvalue, 8)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.05, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library to Original Code Ratio')
    plt.ylabel('Open to Closed Issues Ratio')
    plt.autoscale(enable=True, axis='both', tight=None)
    
    legend_coefficient = plt.legend(["r = " + str(coefficient)], loc='upper right', bbox_to_anchor=(1.0, 1.0))
    legend_coefficient.set_title("Correlation Coefficient")
    legend_coefficient.get_title().set_fontsize('small')
    legend_coefficient.get_title().set_fontweight('bold')
    
    legend_p = plt.legend(["p = " + str(pvalue)], loc='upper right', bbox_to_anchor=(1.0, 0.85))
    legend_p.set_title("Probability Value")
    legend_p.get_title().set_fontsize('small')
    legend_p.get_title().set_fontweight('bold')

    plt.gca().add_artist(legend_coefficient)
    plt.gca().add_artist(legend_p)

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

    coefficient, pvalue = pearsonr(x, y) 
    coefficient = round(coefficient, 8)
    pvalue = round(pvalue, 8)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.05, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library to Original Code Ratio')
    plt.ylabel('Stargazer Count')
    plt.autoscale(enable=True, axis='both', tight=None)
        
    legend_coefficient = plt.legend(["r = " + str(coefficient)], loc='upper right', bbox_to_anchor=(1.0, 1.0))
    legend_coefficient.set_title("Correlation Coefficient")
    legend_coefficient.get_title().set_fontsize('small')
    legend_coefficient.get_title().set_fontweight('bold')
    
    legend_p = plt.legend(["p = " + str(pvalue)], loc='upper right', bbox_to_anchor=(1.0, 0.85))
    legend_p.set_title("Probability Value")
    legend_p.get_title().set_fontsize('small')
    legend_p.get_title().set_fontweight('bold')

    plt.gca().add_artist(legend_coefficient)
    plt.gca().add_artist(legend_p)

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

    coefficient, pvalue = pearsonr(x, y) 
    coefficient = round(coefficient, 8)
    pvalue = round(pvalue, 8)

    # Calculate coefficients, and function for the line of best fit.
    coefficients = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(coefficients)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.05, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel('Library to Original Code Ratio')
    plt.ylabel('Commit Count')
    plt.autoscale(enable=True, axis='both', tight=None)

    legend_coefficient = plt.legend(["r = " + str(coefficient)], loc='upper right', bbox_to_anchor=(1.0, 1.0))
    legend_coefficient.set_title("Correlation Coefficient")
    legend_coefficient.get_title().set_fontsize('small')
    legend_coefficient.get_title().set_fontweight('bold')
    
    legend_p = plt.legend(["p = " + str(pvalue)], loc='upper right', bbox_to_anchor=(1.0, 0.85))
    legend_p.set_title("Probability Value")
    legend_p.get_title().set_fontsize('small')
    legend_p.get_title().set_fontweight('bold')

    plt.gca().add_artist(legend_coefficient)
    plt.gca().add_artist(legend_p)

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
    quality_measure_thresholds["library_to_original_ratio"] = quality_measure(columns["library_to_original_ratio"])
    
    # Write to CSV
    df = pd.DataFrame(quality_measure_thresholds)
    df = df.rename(columns={0: 'repository_url'})
    df = df.rename(columns={1: 'open_closed_ratio'})
    df = df.rename(columns={2: 'commit_count'})
    df = df.rename(columns={3: 'creation_date'})
    df = df.rename(columns={4: 'stargazer_count'})
    df = df.rename(columns={5: 'latest_release'})
    df = df.rename(columns={6: 'library_to_original_ratio'})
    df.to_csv('2023-03-21_thresholds.csv', index=False)

