from scipy.stats import spearmanr, pearsonr
from typing import Dict
from sklearn import preprocessing
import numpy as np
from utils.utils import convert_to_unix_timestamp 
from typing import Any, Dict, List, Tuple
import statistics
import os
from datetime import datetime
from scipy.spatial.distance import squareform, pdist
from scipy.cluster.hierarchy import linkage, fcluster

def normalize_dataset(dataset_columns, input_type):
    """
    Normalizes the numerical data in a dictionary of columns using scikit-learn's preprocessing.normalize function.

    Parameters:
        dataset_columns (dict): A dictionary of columns containing either numerical or tuple data.
        input_type (str): A string indicating the type of input data. If "normal", the function assumes that
            the dictionary values are one-dimensional numpy arrays. If "tuple", the function assumes that the
            dictionary values are lists of tuples where the first element of each tuple is a key and the second
            element is a numerical value to be normalized.

    Returns:
        A dictionary of normalized columns.

    Side effects:
        - Converts date columns to Unix timestamps before normalization.
        - Modifies the input dictionary in-place.
    """
    if input_type == "normal":
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
                    value = convert_to_unix_timestamp(dataset_columns[column][i])
                    dataset_columns[column][i] = value
                    i += 1


            # Case: Numeric Columns
            np_column = np.array(dataset_columns[column]) # extract second values of tuples
            normalized_column = preprocessing.normalize([np_column])
            dataset_columns[column] = normalized_column


    if input_type == "tuple":
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


def add_total_column(extracted_columns, type):
    """
    This function adds a new column to a dictionary of extracted columns.
    The name and values of the new column depend on the 'type' argument passed in.

    Args:
        extracted_columns (dict): A dictionary containing key-value pairs of extracted columns from a dataset
        type (str): A string indicating the type of data being processed; if "code", the function calculates the new codebase size column; if "issue", it calculates the new issue count column.

    Returns:
        extracted_columns (dict): The original dictionary with the new column added.

    """

    # If type is "code", add a new column to the dictionary with the sum of the 'library_codebase_size' and 'original_codebase_size' columns.
    if type == "code":
        library_codebase_size = extracted_columns["library_codebase_size"]
        original_codebase_size = extracted_columns["original_codebase_size"]
        new_column_values = [x + y for x, y in zip(library_codebase_size, original_codebase_size)]
        extracted_columns['total_codebase_size'] = new_column_values

        return extracted_columns

    # If type is "issue", add a new column to the dictionary with the sum of the 'open_issue_count' and 'closed_issue_count' columns.
    if type == "issue":
        open_issues = extracted_columns["open_issue_count"]
        closed_issues = extracted_columns["closed_issue_count"]
        new_column_values = [x + y for x, y in zip(open_issues, closed_issues)]
        extracted_columns['total_issue_count'] = new_column_values

        return extracted_columns
    

def categorize_correlations(corr_matrix, variable_names, corr_type):
    """
    Categorizes the correlations in a correlation matrix into "Very Weak", "Weak", "Moderate", "Strong", and "Very Strong"
    based on the ranges -1.0 to -0.7, -0.7 to -0.5, -0.5 to -0.3, -0.3 to -0.1, 0.1 to 0.3, 0.3 to 0.5, 0.5 to 0.7, and 0.7 to 1.0.

    Parameters:
        corr_matrix (pandas.DataFrame): A correlation matrix.
        variable_names (list): A list of variable names corresponding to the columns of the correlation matrix.

    Returns:
        A dictionary with five keys, "Very Weak", "Weak", "Moderate", "Strong", and "Very Strong",
        each corresponding to a list of tuples representing the names of variables that fall into that category.
        Each tuple includes the variable names and the corresponding correlation coefficient.
    """
    categories = {
        "Very Weak": [],
        "Weak": [],
        "Moderate": [],
        "Strong": [],
        "Very Strong": []
    }

    for i in range(corr_matrix.shape[0]):
        for j in range(i+1, corr_matrix.shape[1]):
            corr = corr_matrix.iloc[i,j]
            if corr <= -0.7 or corr >= 0.7:
                categories["Very Strong"].append(((variable_names[i], variable_names[j]), corr))
            elif corr <= -0.5 or corr >= 0.5:
                categories["Strong"].append(((variable_names[i], variable_names[j]), corr))
            elif corr <= -0.3 or corr >= 0.3:
                categories["Moderate"].append(((variable_names[i], variable_names[j]), corr))
            elif corr <= -0.1 or corr >= 0.1:
                categories["Weak"].append(((variable_names[i], variable_names[j]), corr))
            else:
                categories["Very Weak"].append(((variable_names[i], variable_names[j]), corr))

    if not os.path.exists("out"):
        os.makedirs("out")        

    with open("out" + "/" + datetime.now().isoformat() + "_" +  corr_type + "_" + "categories.txt", 'w') as f:
        for category, values in categories.items():
            f.write(f"{category}:\n")
            for value in values:
                f.write(f"- {value}\n")
            f.write("\n")

    return categories

def cluster_correlation_matrix(corr_matrix, corr_type, n_clusters=2, linkage_method='ward'):
    """
    Clusters a correlation matrix using hierarchical clustering.

    Parameters:
    corr_matrix (pandas.DataFrame): a correlation matrix as a pandas DataFrame
    n_clusters (int): the number of clusters to create
    linkage_method (str): the linkage method to use for clustering (default: 'ward')

    Returns:
    labels (numpy.array): an array of labels indicating which cluster each variable belongs to
    """

    # Convert correlation matrix to distance matrix
    dist_matrix = np.sqrt(1 - np.abs(corr_matrix))

    # Perform hierarchical clustering with specified linkage method
    Z = linkage(squareform(dist_matrix), method=linkage_method)

    # Assign labels to clusters
    labels = fcluster(Z, t=n_clusters, criterion='maxclust')

    if not os.path.exists("out"):
        os.makedirs("out")        

    with open("out" + "/" + datetime.now().isoformat() + "_" + corr_type + "_" + "cluster_output.txt", "w") as f:
        for i in range(1, n_clusters+1):
            f.write(f"Cluster {i}:\n")
            cluster_vars = [col for col, label in zip(corr_matrix.columns, labels) if label == i]
            for var in cluster_vars:
                f.write(f"- {var}\n")
            f.write("\n")

    return labels