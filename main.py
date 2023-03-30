import analysis.analysis as a
import utils.utils as utils 
import utils.github as gh
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
    # dataset = utils.convert_dict_to_dataframe(normalized_dataset)
    # Expects Pandas DataFrame
    # dataset = qm.calculate_quality_scores(dataset, "pearson")
    # dataset = utils.convert_dataframe_to_dict(dataset)

    # columns = ["open_issue_count", "closed_issue_count", "commit_count", 
               #"open_closed_ratio", "stargazer_count", "creation_date", 
               #"latest_release", "original_codebase_size", 
               #"library_codebase_size", "library_to_original_ratio", 
               #"quality_measure", "total_codebase_size", "total_issue_count",
               #"maturity_score", "activity_score"]

    # dataset = utils.create_dictionary(dataset, columns)

    # TODO: Extend Dataset

    ## Numerical Columns

    # get_forks
    # get_pulls
    # get_network_events
    # get_subscribers
    # get_contributors
    # get_deployments
    # get_watchers

    ## Custom Metadata Columns

    # get_network_events
    # get_notifications
    # get_projects

    ## Test Afterwards - Returns an Custom Object, needs a littlebit of work.

    # get_stats_code_frequency
    # get_stats_commit_activity
    # get_stats_contributors
    # get_stats_participation

    #gh.append_data("data/cleaned_dataset.csv", "data/extended_dataset.csv", ["forks_count"])
    pulls = gh.test_github_api("get_views_traffic")
    print(pulls.totalCount)

    #avg = gh.get_mean_additions_per_week("kubernetes", "kubernetes")
    #print(avg)
    ## Create Command Line Interface
    # i.create_commandline_interface(dataset)
    # i.create_commandline_interface(normalized_dataset)


if __name__ == "__main__": 
    main()