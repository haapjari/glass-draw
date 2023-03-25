from scipy.stats import spearmanr, pearsonr
from typing import Dict
from datetime import datetime
from sklearn import preprocessing
import numpy as np
from utils.utils import convert_to_unix_timestamp 

def calculate_spearmanr(x, y):
    """
    Calculate the Spearman rank correlation coefficient between two dictionaries of values.

    Args:
        x (dict): A dictionary with unique identifiers as keys and corresponding values.
        y (dict): A dictionary with unique identifiers as keys and corresponding values.

    Returns:
        tuple: A tuple containing the Spearman rank correlation coefficient and the p-value
            of the correlation.
    """
    x_values = list(x.values())
    y_values = list(y.values())
    coefficient, p = spearmanr(x_values, y_values)
    return coefficient, p


def calculate_pearsonr(x, y):
    """
    Calculate the Pearson correlation coefficient between two dictionaries of values.

    Args:
        x (dict): A dictionary with unique identifiers as keys and corresponding values.
        y (dict): A dictionary with unique identifiers as keys and corresponding values.

    Returns:
        tuple: A tuple containing the Pearson correlation coefficient and the p-value
            of the correlation.
    """
    x_values = list(x.values())
    y_values = list(y.values())
    coefficient, p = pearsonr(x_values, y_values)
    return coefficient, p


def normalize_dataset(dataset_columns):
    """
    Normalize the numeric columns of a dataset to have unit norm,
    and convert date columns to Unix timestamp format.

    Args:
        dataset_columns (dict): A dictionary with column names as keys
            and lists of tuples as values. Each tuple contains a unique
            identifier for the row and the corresponding value for that
            column in that row.

    Returns:
        dict: A dictionary with the same keys as the input `dataset_columns`,
            but with the numeric columns normalized and the date columns
            converted to Unix timestamp format.

    """
    for column in dataset_columns:
        # Case: Ignore Columns
        if column == "repository_name" or column == "repository_url":
            continue

        # Case: Date Columns
        if column == "creation_date" or column == "latest_release":
            i = 0 
            while i < len(dataset_columns[column]):
                key = dataset_columns[column][i][0]
                value = convert_to_unix_timestamp(dataset_columns[column][i][1])
                dataset_columns[column][i] = (key, value)
                i += 1
            continue

        # Case: Numeric Columns
        np_column = np.array([x[1] for x in dataset_columns[column]]) # extract second values of tuples
        normalized_column = preprocessing.normalize([np_column])
        i = 0
        while i < len(dataset_columns[column]):
            dataset_columns[column][i] = (dataset_columns[column][i][0], normalized_column[0][i])
            i += 1
    
    return dataset_columns

# Quality Measure 
# TODO
def calculate_quality_measure(normalized_columns: Dict[str, list]) -> Dict[str, list]:
    # Edge Cases
    # Open & Closed Issue Count = 0 -> skip, means that the issues are not used in the project

    # Case: Smaller Better 
    # Open Closed Ratio 
    # Creation Date 

    # Case: Bigger Better
    # Commit Count
    # Stargazer Count
    # Latest Release

    for column in normalized_columns:
        # Case: Ignore Columns
        if column == "repository_name" or column == "repository_url":
            continue

        if column == "commit_count":
            for value in normalized_columns[column]:
                print(value) 
    
        

    return normalized_columns