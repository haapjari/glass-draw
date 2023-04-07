import src.alys.analysis as analysis
import src.alys.quality as quality
import src.utils.utils as utils
import src.intfc.interface as interface
import src.mdls.repository as repository
import src.plot.plot as plot
import src.ghb.github as github

import pandas as pd
import numpy as np
import csv


def main():
    # Read a File to a Variable.
    # dataset_file = utils.read_csv_file("data/cleaned_dataset.csv")

    # Columns that are going to be extracted from the .csv file.
    # columns = ["repository_name", "repository_url", "open_issue_count",
#                "closed_issue_count", "commit_count", "open_closed_ratio",
               # "stargazer_count", "creation_date", "latest_release",
               # "original_codebase_size", "library_codebase_size",
               # "library_to_original_ratio"]

    # # # Extract the Columns from the File.
    # dataset_columns = utils.extract_columns(dataset_file, columns, "normal")
    # dataset_columns = analysis.add_total_column(dataset_columns, "code")
    # dataset_columns = analysis.add_total_column(dataset_columns, "issue")
    # normalized_dataset = analysis.normalize_dataset(dataset_columns, "normal")

    # TODO: Quality Measure Thing
    # interface.create_commandline_interface(normalized_dataset)

    # Correlation Matrix & Dendogram
    # matrix, names = analysis.correlation_matrix(normalized_dataset, "pearson", ["repository_name", "repository_url"])
    # labels = a.cluster_correlation_matrix(matrix, "pearson", n_clusters=3)
    # visualize_dendrogram(matrix, "pearson")

    # Calculate Quality Measures (Pearson)
    # dataset = utils.convert_dict_to_dataframe(normalized_dataset)
    # Expects Pandas DataFrame
    # dataset = qm.calculate_quality_scores(dataset, "pearson")
    # dataset = utils.convert_dataframe_to_dict(dataset)

    # columns = ["open_issue_count", "closed_issue_count", "commit_count",
    # "open_closed_ratio", "stargazer_count", "creation_date",
    # "latest_release", "original_codebase_size",
    # "library_codebase_size", "library_to_original_ratio",
    # "quality_measure", "total_codebase_size", "total_issue_count",
    # "maturity_score", "activity_score"]

    # dataset = utils.create_dictionary(dataset, columns)

    #
    # TODO: Extend Dataset
    # 

    gh = github.GitHub()

    utils.process_csv_file("data/cleaned_dataset.csv", "data/output.csv", gh)

        # row = next(csv_reader) 
        # parts = row[1].split("/")
        # repo = parts[-1]
        # name = parts[-2]

        # print(f"Repo: {repo}, Name: {name}")
        

        # TODO
        # This is how it's done in the loop.
        # We extract the first element of a row. Each row is a list.
        # for row in csv_reader: 
            # parts = row[1].split("/")

            # repo = parts[-1]
            # name = parts[-2]

            # print(f"Repo: {repo}, Name: {name}")

    
    # Add Columns to the Dataset File
    # Loop through the rows, extract name and owner of the repository
    # Query for additional values and add them to the dataset
    # Save the dataset to a new file

    # gh = github.GitHub()
    # repo = gh.get_repo("kubernetes", "kubernetes")

    # TODO: Add these values to the dataset

    # avg_weekly_additions, avg_weekly_deletions = gh.get_avg_weekly_additions(repo)

    # print(avg_weekly_additions)
    # forks = repo.forks_count
    # pulls = repo.get_pulls().totalCount
    # network_events = repo.get_network_events().totalCount
    # subscribers = repo.get_subscribers().totalCount
    # contributors = repo.get_contributors().totalCount
    # deployments = repo.get_deployments().totalCount
    # watchers = repo.get_watchers().totalCount
    # notifications = repo.get_notifications().totalCount
    # avg addition per contributor per wee
    # avg deletion per contributor per week

    ### --- ###

    # Create Command Line Interface

    # i.create_commandline_interface(dataset)
    # i.create_commandline_interface(normalized_dataset)


if __name__ == "__main__":
    main()
