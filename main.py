from matplotlib.lines import Line2D

import src.alys.analysis as analysis
import src.alys.quality as quality
import src.plot.plot as plot
import numpy as np
from sklearn.preprocessing import MinMaxScaler 
from dotenv import load_dotenv
import psycopg2
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import statsmodels.api as sm
from scipy import stats
from scipy.stats import spearmanr

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

    cur.execute(f"SELECT open_issues, closed_issues, commits, self_written_loc, library_loc, creation_date, stargazers, latest_release, forks, open_pulls, closed_pulls, releases, network_events, subscribers, contributors, watchers FROM {normalized_table}")
    
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
    library_loc_proportion = []

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

    # calculate and populate "library_loc_proportion" with a formula (Library LOC / (Self-Written LOC + Library LOC))
    for i in range(len(library_loc)):
        library_loc_proportion.append(library_loc[i] / (self_written_loc[i] + library_loc[i]))

    data = pd.DataFrame({
        'stargazers': stargazers,
        'forks': forks,
        'subscribers': subscribers,
        'watchers': watchers,
        'open_issues': open_issues,
        'closed_issues': closed_issues,
        'commits': commits,
        'open_pulls': open_pulls,
        'closed_pulls': closed_pulls,
        'network_events': network_events,
        'contributors': contributors,
        'creation_date': creation_date,
        'latest_release': latest_release,
        'releases': releases,
    })

    # Calculate composite scores for each group of metrics
    popularity_score = data.iloc[:, :4].sum(axis=1)
    activity_score = data.iloc[:, 4:11].sum(axis=1)
    maturity_score = data.iloc[:, 11:].sum(axis=1)

    # Combine the composite scores into a single DataFrame
    composite_scores = pd.DataFrame({
        'popularity_score': popularity_score,
        'activity_score': activity_score,
        'maturity_score': maturity_score,
        'library_loc_proportion': library_loc_proportion
    })

    correlation_matrix, p_value_matrix = spearmanr(composite_scores)

    # Extract the correlation coefficients and p-values for each independent variable
    correlations = correlation_matrix[-1, :-1]
    p_values = p_value_matrix[-1, :-1]

    print("Coefficients: ", correlations)
    print("Probability Values:", p_values)

    variable_names = ['Popularity', 'Activity', 'Maturity']

    # Create bar plot for correlation coefficients
    plt.figure(figsize=(8, 4))
    plt.bar(variable_names, correlations)
    plt.ylabel("Spearman's Rank Correlation Coefficient")

    plt.axhline(y=0.00, color='black', linestyle='--', linewidth=0.5)

    # Save the correlation coefficients plot
    if not os.path.exists("out"):
        os.makedirs("out")
    file_name = f"{datetime.now().isoformat()}_spearman_correlation_coefficients.png"
    plt.savefig(f"out/{file_name}")
    plt.close()

    # print("Variable Names: ", variable_names)
    # print("P-Values: ", p_values)

    # # Create bar plot for p-values

    # plt.figure(figsize=(8, 4))
    # plt.bar(variable_names, p_values)
    # plt.axhline(y=significance_level, color='r', linestyle='--')
    # plt.ylabel('Probability Values')
    # plt.yscale('log')

    # # Create custom legend
    # legend_elements = [
    #     Line2D([0], [0], color='r', linestyle='--', lw=2, label=f"Significance level ({significance_level})")]
    # plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 0.95))

    # # Save the p-values plot
    # if not os.path.exists("out"):
    #     os.makedirs("out")
    # file_name = f"{datetime.now().isoformat()}_spearman_p_values_log_scale.png"
    # plt.savefig(f"out/{file_name}")
    # plt.close()

    # Close the Cursor and Connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
