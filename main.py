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
    # 1. Calculate Quality Measures (Pearson, Kendall, Spearman)
    # --------------------------------------------------------- #
    
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

    # Define your column names
    # popularity_columns = ['stargazers', 'forks', 'subscribers', 'watchers']
    # activity_columns = ['open_issues', 'closed_issues', 'commits', 'open_pulls', 'closed_pulls', 'network_events', 'contributors']
    # maturity_columns = ['creation_date', 'latest_release', 'releases']

    # lists = [("Open Issues", open_issues), ("Closed Issues", closed_issues), ("Commits", commits), ("Self Written LOC", self_written_loc), ("Library LOC", library_loc), ("Creation Date", creation_date), ("Stargazers", stargazers), ("Latest Release", latest_release), ("Forks", forks), ("Open Pulls", open_pulls), ("Closed Pulls", closed_pulls), ("Releases", releases), ("Network Events", network_events), ("Subscribers", subscribers), ("Contributors", contributors), ("Watchers", watchers)]

    # calculate and populate "library_loc_proportion" with a formula (Library LOC / (Self-Written LOC + Library LOC))
    for i in range(len(library_loc)):
        library_loc_proportion.append(library_loc[i] / (self_written_loc[i] + library_loc[i]))

    # lists = [("Library LOC Proportion", library_loc_proportion), ("Self-Written LOC", self_written_loc), ("Library LOC", library_loc), ("Open Issues", open_issues), ("Closed Issues", closed_issues), ("Commits", commits), ("Creation Date", creation_date), ("Stargazers", stargazers), ("Latest Release", latest_release), ("Forks", forks), ("Open Pulls", open_pulls), ("Closed Pulls", closed_pulls), ("Releases", releases), ("Network Events", network_events), ("Subscribers", subscribers), ("Contributors", contributors), ("Watchers", watchers)]

    # ---
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

    # Call the model
    independent_vars = [popularity_score, activity_score, maturity_score]
    dependent_var = library_loc_proportion
    column_names = ['Popularity', 'Activity', 'Maturity', 'Library LOC Proportion']

    model = analysis.multiple_linear_regression(independent_vars, dependent_var, column_names)

    print("Intercept: ", model.intercept_)
    print("Coefficients: ", model.coef_)

    # plt.bar(column_names[:-1], model.coef_)
    # plt.xlabel('Independent Variables')
    # plt.ylabel('Coefficients')
    # plt.title('Multiple Linear Regression Coefficients')
    #
    # # Create "out" folder if it doesn't exist
    # if not os.path.exists("out"):
    #     os.makedirs("out")

    # # Save the plot to the "out" folder
    # file_name = f"{datetime.now().isoformat()}_regression_model_coefficients.png"
    # plt.savefig(f"out/{file_name}")

    X = sm.add_constant(np.column_stack(independent_vars))
    y = dependent_var
    model_sm = sm.OLS(y, X).fit()

    p_values = model_sm.pvalues[1:]  # Exclude the intercept
    # print("P-values:", p_values)

    # ---

    significance_level = 0.05


    #analysis.visualize("Open Issues", open_issues)

    # plot.plot("spearman", self_written_loc, "Self Written LOC", open_issues, "Open Issues")

    # plot.plot("spearman", library_loc, "Library LOC", open_issues, "Open Issues")

    # spearman_corr_matrix = analysis.correlation_heatmap(lists, "spearman")
    # kendall_corr_matrix = analysis.correlation_heatmap(lists, "kendall")
    # pearson_corr_matrix = analysis.correlation_heatmap(lists, "pearson")
    
    # spearman_corr_categories = analysis.categorize_correlations(lists, "spearman") 
    # kendall_corr_categories = analysis.categorize_correlations(lists, "kendall")
    # pearson_corr_categories = analysis.categorize_correlations(lists, "pearson")
    
    # plot.visualize_dendrogram(lists, "spearman")
    # plot.visualize_dendrogram(lists, "pearson")
    # plot.visualize_dendrogram(lists, "kendall")

# Close the Cursor and Connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
