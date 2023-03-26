from scipy.stats import spearmanr, pearsonr
from typing import Dict
from sklearn import preprocessing
import numpy as np
from utils.utils import convert_to_unix_timestamp 
from typing import Any, Dict, List, Tuple
import statistics

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
        # Convert Numeric Values to Unix Timestamps
        # Normalization is then happening in the "Numeric Columns"
        if column == "creation_date" or column == "latest_release":
            i = 0 
            while i < len(dataset_columns[column]):
                key = dataset_columns[column][i][0]
                value = convert_to_unix_timestamp(dataset_columns[column][i][1])
                dataset_columns[column][i] = (key, value)
                i += 1


        # Case: Numeric Columns
        np_column = np.array([x[1] for x in dataset_columns[column]]) # extract second values of tuples
        normalized_column = preprocessing.normalize([np_column])
        i = 0
        while i < len(dataset_columns[column]):
            dataset_columns[column][i] = (dataset_columns[column][i][0], normalized_column[0][i])
            i += 1
    
    return dataset_columns


def adjust_normalized_columns(normalized_columns: Dict[str, List[Tuple[Any, float]]]) -> Dict[str, List[Tuple[Any, float]]]:
    """
    Adjusts the values of certain columns in a dictionary of normalized columns based on whether smaller or bigger values
    are considered better for each column. Specifically, it flips the values for columns where smaller values are considered
    better (i.e. "open_closed_ratio" and "creation_date"), so that the distance from 0 represents the quality measure (with
    0 being the worst and 1 being the best). This ensures that all values in the dictionary are on the same scale, with higher
    values always indicating better quality.

    Args:
        normalized_columns (Dict[str, List[Tuple[Any, float]]]): A dictionary containing the normalized columns to adjust.

    Returns:
        Dict[str, List[Tuple[Any, float]]]: The adjusted dictionary of normalized columns.

    """
    # Loop through each column in the dictionary
    for column in normalized_columns:
        # If the column is "open_closed_ratio" or "creation_date", flip the values
        if column == "open_closed_ratio" or column == "creation_date":
            i = 0
            while i < len(normalized_columns[column]):
                key = normalized_columns[column][i][0]
                value = 1 - normalized_columns[column][i][1]
                normalized_columns[column][i] = (key, value)
                i += 1    
            continue

    # Return the adjusted dictionary
    return normalized_columns

def calculate_quality_measures(repos):
    """
    Calculates the quality measure for each repository in the given list.
    
    Args:
    - repos: A list of Repo objects to calculate the quality measure for.

    Returns:
    - repos: list with the quality_measure values
    """

    for repo in repos:
        # Gather the values to calculate the quality measure
        values = []
        values.append(repo.commit_count)
        values.append(repo.open_closed_ratio)
        values.append(repo.stargazer_count)
        values.append(repo.creation_date)
        values.append(repo.latest_release)

        # Calculate the mean of the values
        repo.quality_measure = statistics.mean(values)

    return repos
