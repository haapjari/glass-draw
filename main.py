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

    lists = [("open_issues", open_issues), ("closed_issues", closed_issues), ("commits", commits), ("self_written_loc", self_written_loc), ("library_loc", library_loc), ("creation_date", creation_date), ("stargazers", stargazers), ("latest_release", latest_release), ("forks", forks), ("open_pulls", open_pulls), ("closed_pulls", closed_pulls), ("releases", releases), ("network_events", network_events), ("subscribers", subscribers), ("contributors", contributors), ("watchers", watchers), ("self_written_to_library_loc_ratio", self_written_to_library_loc_ratio), ("library_to_self_written_loc_ratio", library_to_self_written_loc_ratio), ("open_to_total_issues_ratio", open_to_total_issues_ratio), ("open_to_total_pulls_ratio", open_to_total_pulls_ratio)] 

    # spearman_corr_matrix = analysis.correlation_heatmap(lists, "spearman")
    # kendall_corr_matrix = analysis.correlation_heatmap(lists, "kendall")
    # pearson_corr_matrix = analysis.correlation_heatmap(lists, "pearson")

    # spearman_corr_categories = analysis.categorize_correlations(lists, "spearman") 
    # kendall_corr_categories = analysis.categorize_correlations(lists, "kendall")
    # pearson_corr_categories = analysis.categorize_correlations(lists, "pearson")

    # plot.visualize_dendrogram(lists, "spearman")
    # plot.visualize_dendrogram(lists, "pearson")
    # plot.visualize_dendrogram(lists, "kendall")

    # ---------------------------------- #
    # Calculate: Spearman Quality Scores #
    # ---------------------------------- #

    # Quality Score: "Development Efficiency"

    # qs_spearman_efficiency = {}

    # qs_spearman_efficiency["creation_date"] = creation_date
    # qs_spearman_efficiency["commits"] = commits
    # qs_spearman_efficiency["latest_release"] = latest_release                                 
    # qs_spearman_efficiency["creation_date"] = creation_date                                  
    # qs_spearman_efficiency["releases"] = releases                                           

    # qs_spearman_efficiency_score = quality.calculate_qs_spearman_efficiency(qs_spearman_efficiency)

    # # Quality Score: "Popularity"

    # qs_spearman_popularity = {}
   
    # qs_spearman_popularity["network_events"] = network_events
    # qs_spearman_popularity["forks"] = forks
    # qs_spearman_popularity["subscribers"] = subscribers
    # qs_spearman_popularity["watchers"] = watchers
    # qs_spearman_popularity["stargazers"] = stargazers

    # qs_spearman_popularity_score = quality.calculate_qs_spearman_popularity(qs_spearman_popularity)

    # # Quality Score: "Responsiveness"

    # qs_spearman_responsiveness = {}

    # qs_spearman_responsiveness["open_to_total_pulls_ratio"] = open_to_total_pulls_ratio
    # qs_spearman_responsiveness["open_to_total_issues_ratio"] = open_to_total_issues_ratio

    # qs_spearman_responsiveness_score = quality.calculate_qs_spearman_responsiveness(qs_spearman_responsiveness)

    # # Quality Measure

    # efficiency_weight = 0.3333
    # responsiveness_weight = 0.3333
    # popularity_weight = 0.3333

    # weights = np.array([efficiency_weight, responsiveness_weight, popularity_weight])

    # qm_spearman = np.average([qs_spearman_efficiency_score, qs_spearman_responsiveness_score, qs_spearman_popularity_score], axis=0, weights=weights)

    # qm_spearman_lists = [("Efficiency Score", qs_spearman_efficiency_score), ("Responsiveness Score", qs_spearman_responsiveness_score), ("Popularity Score", qs_spearman_popularity_score), ("Quality Measure", qm_spearman), ("Self Written LOC", self_written_loc), ("Library LOC", library_loc), ("Library to Self Written LOC Ratio", library_to_self_written_loc_ratio)]

    # spearman_corr_matrix = analysis.correlation_heatmap(qm_spearman_lists, "spearman")

    # ---------------------------------- #
    # Calculate: Kendall Quality Scores  #
    # ---------------------------------- #

    # Quality Score: "Development Efficiency"

    qs_kendall_efficiency = {}

    qs_kendall_efficiency["creation_date"] = creation_date
    qs_kendall_efficiency["commits"] = commits
    qs_kendall_efficiency["latest_release"] = latest_release
    qs_kendall_efficiency["creation_date"] = creation_date
    qs_kendall_efficiency["releases"] = releases

    qs_kendall_efficiency_score = quality.calculate_qs_kendall_efficiency(qs_kendall_efficiency)

    # qs_spearman_popularity_score = quality.calculate_qs_spearman_popularity(qs_spearman_popularity)

    # Quality Score: 2 "Popularity"

    qs_kendall_popularity = {}

    qs_kendall_popularity["network_events"] = network_events
    qs_kendall_popularity["forks"] = forks
    qs_kendall_popularity["subscribers"] = subscribers
    qs_kendall_popularity["watchers"] = watchers
    qs_kendall_popularity["stargazers"] = stargazers

    qs_kendall_popularity_score = quality.calculate_qs_kendall_popularity(qs_kendall_popularity)

    # Quality Score: 3 "Responsiveness"

    qs_kenall_responsiveness = {}

    qs_kenall_responsiveness["open_to_total_pulls_ratio"] = open_to_total_pulls_ratio
    qs_kenall_responsiveness["open_to_total_issues_ratio"] = open_to_total_issues_ratio

    qs_kendall_responsiveness_score = quality.calculate_qs_kendall_responsiveness(qs_kenall_responsiveness)

    # Quality Measure

    efficiency_weight = 0.3333
    responsiveness_weight = 0.3333
    popularity_weight = 0.3333

    weights = np.array([efficiency_weight, responsiveness_weight, popularity_weight])

    qm_kendall = np.average([qs_kendall_efficiency_score, qs_kendall_responsiveness_score, qs_kendall_popularity_score], axis=0, weights=weights)

    qm_kendall_lists = [("Efficiency Score", qs_kendall_efficiency_score), ("Responsiveness Score", qs_kendall_responsiveness_score), ("Popularity Score", qs_kendall_popularity_score), ("Quality Measure", qm_kendall), ("Self Written LOC", self_written_loc), ("Library LOC", library_loc), ("Library to Self Written LOC Ratio", library_to_self_written_loc_ratio)]

    kendall_corr_matrix = analysis.correlation_heatmap(qm_kendall_lists, "kendall")

    # Close the Cursor and Connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
