import src.alys.analysis as analysis
import src.alys.quality as quality
import src.utils.utils as utils
import src.intfc.interface as interface
import src.mdls.repository as repository
import src.plot.plot as plot
import src.ghb.github as github 

import pandas              as pd
import numpy               as np


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
    dataset_columns = analysis.add_total_column(dataset_columns, "code")
    dataset_columns = analysis.add_total_column(dataset_columns, "issue")
    normalized_dataset = analysis.normalize_dataset(dataset_columns, "normal")

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
    # get_notifications

    ## Test Afterwards - Returns an Custom Object, needs a littlebit of work.

    # get_stats_code_frequency
    # Retrieve a list of commits and the number of lines of code that were added
    # and deleted in each commit for a specific repository.

    # get_stats_commit_activity
    # get_stats_contributors
    # get_stats_participation

    #gh.append_data("data/cleaned_dataset.csv", "data/extended_dataset.csv", ["forks_count"])
    
    gh = github.GitHub()
    repo = gh.get_repo("kubernetes", "kubernetes")

    print(repo.forks_count)
    
    # pulls = gh.test_github_api("get_notifications")
    # print(pulls.totalCount)

    #avg = gh.get_mean_additions_per_week("kubernetes", "kubernetes")
    #print(avg)
    ## Create Command Line Interface
    # i.create_commandline_interface(dataset)
    # i.create_commandline_interface(normalized_dataset)


if __name__ == "__main__": 
    main()