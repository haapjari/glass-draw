import src.alys.analysis as analysis
# import src.alys.quality as quality
# import src.utils.utils as utils
# import src.intfc.interface as interface
# import src.mdls.repository as repository
import src.plot.plot as plot
# import src.ghb.github as github
# import pandas as pd
# import numpy as np
# import csv

from dotenv import load_dotenv
import psycopg2
import os


def main():
    # --------------------------------------------------------- #
    # 1. Read Dataset from the Database
    # --------------------------------------------------------- #

    load_dotenv()

    # PostgreSQL Credentials
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    # Connect to PostgreSQL Database
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB
    )

    # Create a Cursor Object to Execute Queries
    cur = conn.cursor()

    table = "repos"
    normalized_table = "normalized_repos"
    
    # --------------------------------------------------------- #
    # 2. Calculate Quality Measures (Pearson, Kendall, Spearman)
    # --------------------------------------------------------- #
    
    cur.execute(f"SELECT open_issues, closed_issues, commits, self_written_loc, library_loc, creation_date, stargazers, latest_release, forks, open_pulls, closed_pulls, releases, network_events, subscribers, contributors, watchers, library_to_total_loc_ratio, open_to_total_issues_ratio, open_to_total_pulls_ratio FROM {normalized_table}")
    
    rows = cur.fetchall()

    open_issues = []
    closed_issues = []
    commits = []
    self_written_loc = []
    library_loc = []
    creation_date = []
    stargazers = []
    latest_release = []
    forks = []
    open_pulls = []
    closed_pulls = []
    releases = []
    network_events = []
    subscribers = []
    contributors = []
    watchers = []
    library_to_total_loc_ratio = []
    open_to_total_issues_ratio = []
    open_to_total_pulls_ratio = []

    for row in rows:
        open_issues.append(row[0]) 
        closed_issues.append(row[1])
        commits.append(row[2])
        self_written_loc.append(row[3])
        library_loc.append(row[4])
        creation_date.append(row[5])
        stargazers.append(row[6])
        latest_release.append(row[7])
        forks.append(row[8])
        open_pulls.append(row[9])
        closed_pulls.append(row[10])
        releases.append(row[11])
        network_events.append(row[12])
        subscribers.append(row[13])
        contributors.append(row[14])
        watchers.append(row[15])
        library_to_total_loc_ratio.append(row[16])
        open_to_total_issues_ratio.append(row[17])
        open_to_total_pulls_ratio.append(row[18])

        lists = [("open_issues", open_issues), ("closed_issues", closed_issues), ("commits", commits), ("self_written_loc", self_written_loc), ("library_loc", library_loc), ("creation_date", creation_date), ("stargazers", stargazers), ("latest_release", latest_release), ("forks", forks), ("open_pulls", open_pulls), ("closed_pulls", closed_pulls), ("releases", releases), ("network_events", network_events), ("subscribers", subscribers), ("contributors", contributors), ("watchers", watchers), ("library_to_total_loc_ratio", library_to_total_loc_ratio), ("open_to_total_issues_ratio", open_to_total_issues_ratio), ("open_to_total_pulls_ratio", open_to_total_pulls_ratio)]

    # spearman_corr_matrix = analysis.correlation_heatmap(lists, "spearman")
    # kendall_corr_matrix = analysis.correlation_heatmap(lists, "kendall")
    # pearson_corr_matrix = analysis.correlation_heatmap(lists, "pearson")

    # spearman_corr_categories = analysis.categorize_correlations(lists, "spearman") 
    # kendall_corr_categories = analysis.categorize_correlations(lists, "kendall")
    # pearson_corr_categories = analysis.categorize_correlations(lists, "pearson")

    # plot.visualize_dendrogram(lists, "spearman")
    # plot.visualize_dendrogram(lists, "pearson")
    # plot.visualize_dendrogram(lists, "kendall")

    # Pearson Quality Scores
    # ----------------------
    
    # Quality Score: 1 "Project Health"

    # open_to_total_pulls_ratio
    # open_to_total_issues_ratio
    # latest_release
    # creation_date
    # releases

    # Quality Score: 2 "Community Engagement"

    # contributors
    # commits
    # network_events
    # forks
    # subscribers
    # watchers
    # stargazers

    # Spearman Quality Scores
    # -----------------------

    # Quality Score: "Development Efficiency"

    # library_to_total_loc_ratio
    # creation_date
    # commits
    # contributors
    # releases
    # latest_release

    # Quality Score: 2 "Popularity"

    # network_events
    # forks
    # subscribers
    # watchers 
    # stargazers

    # Quality Score: 3 "Responsiveness"

    # open_to_total_pulls_ratio
    # open_to_total_issues_ratio

    # Kendall Quality Scores
    # ----------------------

    # Quality Score: "Development Efficiency"

    # library_to_total_loc_ratio
    # creation_date
    # commits
    # contributors
    # releases
    # latest_release

    # Quality Score: 2 "Popularity"

    # network_events
    # forks
    # subscribers
    # watchers 
    # stargazers

    # Quality Score: 3 "Responsiveness"

    # open_to_total_pulls_ratio
    # open_to_total_issues_ratio

    #   - Qualitative Reasoning for the Quality Score Names
    #   - Calculate Quality Scores
    #   - Calculate Quality Measures

    # Close the Cursor and Connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
