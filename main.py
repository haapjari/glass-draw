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

    cur.execute(f"SELECT repo_id, self_written_loc, library_loc FROM {table}")
    rows = cur.fetchall() 

    self_written_to_library_loc_ratio = {} 

    # TODO: Calculate Self-Written to Library LOC Ratio.

    # for row in rows:
    #     print(row)
    #     id = row[0]
    #     self_written_loc = row[1]
    #     library_loc = row[2]
    #     self_written_to_library_loc_ratio[id] = self_written_loc / library_loc

    # for row in self_written_to_library_loc_ratio.items():
    #     print(row) 

    # ratios_array = np.array(list(self_written_to_library_loc_ratio.values())).reshape(-1, 1)

    # Convert the dictionary of ratios into a NumPy array and reshape it into a 2D array
    # ratios_array = np.array(list(self_written_to_library_loc_ratio.values())).reshape(-1, 1)

    # Create a MinMaxScaler instance
    # scaler = MinMaxScaler()

    # Fit the scaler to the data and transform the data using the scaler
    # normalized_ratios_array = scaler.fit_transform(ratios_array)

    # Convert the normalized NumPy array back to a dictionary
    # normalized_ratios = {repo_id: float(ratio) for repo_id, ratio in zip(self_written_to_library_loc_ratio.keys(), normalized_ratios_array)}

    # --------------------------------------------------------- #
    # 2. Calculate Quality Measures (Pearson, Kendall, Spearman)
    # --------------------------------------------------------- #
    
    # cur.execute(f"SELECT open_issues, closed_issues, commits, self_written_loc, library_loc, creation_date, stargazers, latest_release, forks, open_pulls, closed_pulls, releases, network_events, subscribers, contributors, watchers, library_to_total_loc_ratio, open_to_total_issues_ratio, open_to_total_pulls_ratio FROM {normalized_table}")
    # 
    # rows = cur.fetchall()

    # open_issues = []
    # closed_issues = []
    # commits = []
    # self_written_loc = []
    # library_loc = []
    # creation_date = []
    # stargazers = []
    # latest_release = []
    # forks = []
    # open_pulls = []
    # closed_pulls = []
    # releases = []
    # network_events = []
    # subscribers = []
    # contributors = []
    # watchers = []
    # library_to_self_written_loc_ratio = []
    # open_to_total_issues_ratio = []
    # open_to_total_pulls_ratio = []

    # for row in rows:
    #     open_issues.append(row[0]) 
    #     closed_issues.append(row[1])
    #     commits.append(row[2])
    #     self_written_loc.append(row[3])
    #     library_loc.append(row[4])
    #     creation_date.append(row[5])
    #     stargazers.append(row[6])
    #     latest_release.append(row[7])
    #     forks.append(row[8])
    #     open_pulls.append(row[9])
    #     closed_pulls.append(row[10])
    #     releases.append(row[11])
    #     network_events.append(row[12])
    #     subscribers.append(row[13])
    #     contributors.append(row[14])
    #     watchers.append(row[15])
    #     library_to_total_loc_ratio.append(row[16])
    #     open_to_total_issues_ratio.append(row[17])
    #     open_to_total_pulls_ratio.append(row[18])

    #     lists = [("open_issues", open_issues), ("closed_issues", closed_issues), ("commits", commits), ("self_written_loc", self_written_loc), ("library_loc", library_loc), ("creation_date", creation_date), ("stargazers", stargazers), ("latest_release", latest_release), ("forks", forks), ("open_pulls", open_pulls), ("closed_pulls", closed_pulls), ("releases", releases), ("network_events", network_events), ("subscribers", subscribers), ("contributors", contributors), ("watchers", watchers), ("library_to_total_loc_ratio", library_to_total_loc_ratio), ("open_to_total_issues_ratio", open_to_total_issues_ratio), ("open_to_total_pulls_ratio", open_to_total_pulls_ratio)]

    # TODO: Create Matrix / Categories Again, with the "Self-Written to Library LOC Ratio"

    # # spearman_corr_matrix = analysis.correlation_heatmap(lists, "spearman")
    # # kendall_corr_matrix = analysis.correlation_heatmap(lists, "kendall")
    # # pearson_corr_matrix = analysis.correlation_heatmap(lists, "pearson")

    # # spearman_corr_categories = analysis.categorize_correlations(lists, "spearman") 
    # # kendall_corr_categories = analysis.categorize_correlations(lists, "kendall")
    # # pearson_corr_categories = analysis.categorize_correlations(lists, "pearson")

    # # plot.visualize_dendrogram(lists, "spearman")
    # # plot.visualize_dendrogram(lists, "pearson")
    # # plot.visualize_dendrogram(lists, "kendall")

    # # Pearson Quality Scores
    # # ----------------------
    # 
    # # Quality Score: 1 "Project Health"

    # # open_to_total_pulls_ratio
    # # open_to_total_issues_ratio
    # # latest_release
    # # creation_date
    # # releases

    # # Quality Score: 2 "Community Engagement"

    # # contributors
    # # commits
    # # network_events
    # # forks
    # # subscribers
    # # watchers
    # # stargazers

    # # Spearman Quality Scores
    # # -----------------------

    # # Quality Score: "Development Efficiency"

    # # library_to_total_loc_ratio
    # # creation_date
    # # commits
    # # contributors
    # # releases
    # # latest_release

    # # Quality Score: 2 "Popularity"

    # # network_events
    # # forks
    # # subscribers
    # # watchers 
    # # stargazers

    # # Quality Score: 3 "Responsiveness"

    # # open_to_total_pulls_ratio
    # # open_to_total_issues_ratio

    # # Kendall Quality Scores
    # # ----------------------

    # # Quality Score: "Development Efficiency"

    # # library_to_total_loc_ratio
    # # creation_date
    # # commits
    # # contributors
    # # releases
    # # latest_release

    # # Quality Score: 2 "Popularity"

    # # network_events
    # # forks
    # # subscribers
    # # watchers 
    # # stargazers

    # # Quality Score: 3 "Responsiveness"

    # # open_to_total_pulls_ratio
    # # open_to_total_issues_ratio

    # # --------------------------------------------------------- #
    # # 3. Calculate Quality Scores
    # # --------------------------------------------------------- #

    # #   - Qualitative Reasoning for the Quality Score Names
    # #   - Calculate Quality Scores
    # #   - Calculate Quality Measures

    # # --------------------------------------------------------- #
   
    # # Pearson Quality Scores
    # # ----------------------
    # 
    # # Quality Score: 1 "Health"

    # # open_to_total_pulls_ratio - smaller is better
    # # open_to_total_issues_ratio - smaller is better
    # # latest_release - bigger is better
    # # creation_date - smaller is better
    # # releases - bigger is better

    # qs_pearson_health = {}

    # qs_pearson_health["open_to_total_pulls_ratio"] = open_to_total_pulls_ratio
    # qs_pearson_health["open_to_total_issues_ratio"] = open_to_total_issues_ratio
    # qs_pearson_health["latest_release"] = latest_release
    # qs_pearson_health["creation_date"] = creation_date
    # qs_pearson_health["releases"] = releases

    # qs_pearson_health_score = quality.calculate_qs_pearson_health(qs_pearson_health)
    # 
    # # print("Pearson Health Score: ", qs_pearson_health_score)

    # # Quality Score: 2 "Engagement" - bigger is better

    # # contributors
    # # commits
    # # network_events
    # # forks
    # # subscribers
    # # watchers
    # # stargazers

    # qs_pearson_engagement = {}
    # qs_pearson_engagement["contributors"] = contributors
    # qs_pearson_engagement["commits"] = commits
    # qs_pearson_engagement["network_events"] = network_events
    # qs_pearson_engagement["forks"] = forks
    # qs_pearson_engagement["subscribers"] = subscribers
    # qs_pearson_engagement["watchers"] = watchers
    # qs_pearson_engagement["stargazers"] = stargazers

    # qs_pearson_engagement_score = quality.calculate_qs_pearson_engagement(qs_pearson_engagement)

    # # print("Pearson Engagement Score: ", qs_pearson_engagement_score)
    # 
    # #: Correlation Matrix for Pearson Quality Scores 

    # engagement_weight = 0.5
    # health_weight = 0.5

    # qm_pearson = [(a * engagement_weight + b * health_weight) for a, b in zip(qs_pearson_health_score, qs_pearson_engagement_score)]

    # # Correlation Matrix: Pearson Quality Scores
    # # ------------------------------------------

    # # self_written_loc
    # # library_loc
    # # qs_pearson_health_score
    # # qs_pearson_engagement_score
    # # qm_pearson

    # qm_pearson_lists = [("self_written_loc", self_written_loc), ("library_loc", library_loc), ("health_score", qs_pearson_health_score), ("engagement_score", qs_pearson_engagement_score), ("quality measure", qm_pearson)]

    # pearson_corr_matrix = analysis.correlation_heatmap(qm_pearson_lists, "pearson")

    # Close the Cursor and Connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
