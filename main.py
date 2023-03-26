import analysis.analysis as a
import utils.utils as utils 
import interface.interface as i
from models.repository import extract_repositories
from plot.plot import plot, heatmap, correlation_matrix, visualize_categories, visualize_dendrogram
import pandas as pd
import numpy as np
import qm.qm as qm

def main():
    # Read a File to a Variable.
    dataset_file = utils.read_csv_file("data/cleaned_dataset.csv")

    # Columns that are going to be extracted from the .csv file.
    columns = ["repository_name", "repository_url", "open_issue_count", 
               "closed_issue_count", "commit_count", "open_closed_ratio", 
               "stargazer_count", "creation_date", "latest_release", 
               "original_codebase_size", "library_codebase_size", 
               "library_to_original_ratio"]

    # Extract the Columns from the File.
    dataset_columns = utils.extract_columns(dataset_file, columns, "normal")
    dataset_columns = a.add_total_column(dataset_columns, "code")
    dataset_columns = a.add_total_column(dataset_columns, "issue")
    normalized_dataset = a.normalize_dataset(dataset_columns, "normal")

    # TODO: Quality Measure Thing
    # i.create_commandline_interface(normalized_dataset) 

    # Correlation Matrix & Dendogram
    #matrix, names = correlation_matrix(normalized_dataset, "pearson", ["repository_name", "repository_url"])
    #labels = a.cluster_correlation_matrix(matrix, "pearson", n_clusters=3)
    #visualize_dendrogram(matrix, "pearson")     

    # Calculate Quality Measures (Pearson)
    dataset = utils.convert_dict_to_dataframe(normalized_dataset)
    # Expects Pandas DataFrame
    dataset = qm.calculate_quality_scores(dataset, "pearson")
    dataset = utils.convert_dataframe_to_dict(dataset)

    columns = ["open_issue_count", "closed_issue_count", "commit_count", 
               "open_closed_ratio", "stargazer_count", "creation_date", 
               "latest_release", "original_codebase_size", 
               "library_codebase_size", "library_to_original_ratio", 
               "quality_measure", "total_codebase_size", "total_issue_count",
               "maturity_score", "activity_score"]

    dataset = utils.create_dictionary(dataset, columns)

    # Create Command Line Interface
    i.create_commandline_interface(dataset)
    # i.create_commandline_interface(normalized_dataset)


if __name__ == "__main__": 
    main()