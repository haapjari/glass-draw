import src.alys.analysis as analysis
import src.alys.quality as quality
import src.plot.plot as plot
import numpy as np
from sklearn.preprocessing import MinMaxScaler 
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
    # 1. Calculate Quality Measures (Pearson, Kendall, Spearman)
    # --------------------------------------------------------- #
    
    cur.execute(f"SELECT open_issues, closed_issues, commits, self_written_loc, library_loc, creation_date, stargazers, latest_release, forks, open_pulls, closed_pulls, releases, network_events, subscribers, contributors, watchers, self_written_to_library_loc_ratio, library_to_self_written_loc_ratio, open_to_total_issues_ratio, open_to_total_pulls_ratio FROM {normalized_table}")
    
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
    self_written_to_library_loc_ratio = []
    library_to_self_written_loc_ratio = []
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
        self_written_to_library_loc_ratio.append(row[16])
        library_to_self_written_loc_ratio.append(row[17])
        open_to_total_issues_ratio.append(row[18])
        open_to_total_pulls_ratio.append(row[19])

    lists = [("Open Issues", open_issues), ("Closed Issues", closed_issues), ("Commits", commits), ("Self Written LOC", self_written_loc), ("Library LOC", library_loc), ("Creation Date", creation_date), ("Stargazers", stargazers), ("Latest Release", latest_release), ("Forks", forks), ("Open Pulls", open_pulls), ("Closed Pulls", closed_pulls), ("Releases", releases), ("Network Events", network_events), ("Subscribers", subscribers), ("Contributors", contributors), ("Watchers", watchers)] 

    analysis.visualize("Open Issues", open_issues) 
    analysis.visualize("Closed Issues", closed_issues)
    analysis.visualize("Commits", commits)
    analysis.visualize("Self Written LOC", self_written_loc)
    analysis.visualize("Library LOC", library_loc)
    analysis.visualize("Creation Date", creation_date)
    analysis.visualize("Stargazers", stargazers)
    analysis.visualize("Latest Release", latest_release)
    analysis.visualize("Forks", forks)
    analysis.visualize("Open Pulls", open_pulls)
    analysis.visualize("Closed Pulls", closed_pulls)
    analysis.visualize("Releases", releases)
    analysis.visualize("Network Events", network_events)
    analysis.visualize("Subscribers", subscribers)
    analysis.visualize("Contributors", contributors)
    analysis.visualize("Watchers", watchers)

#     spearman_corr_matrix = analysis.correlation_heatmap(lists, "spearman")
#     kendall_corr_matrix = analysis.correlation_heatmap(lists, "kendall")
#     pearson_corr_matrix = analysis.correlation_heatmap(lists, "pearson")
# 
#     spearman_corr_categories = analysis.categorize_correlations(lists, "spearman") 
#     kendall_corr_categories = analysis.categorize_correlations(lists, "kendall")
#     pearson_corr_categories = analysis.categorize_correlations(lists, "pearson")
# 
#     plot.visualize_dendrogram(lists, "spearman")
#     plot.visualize_dendrogram(lists, "pearson")
#     plot.visualize_dendrogram(lists, "kendall")
# 
    # Close the Cursor and Connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
