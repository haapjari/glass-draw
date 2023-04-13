# import src.alys.analysis as analysis
# import src.alys.quality as quality
# import src.utils.utils as utils
# import src.intfc.interface as interface
# import src.mdls.repository as repository
# import src.plot.plot as plot
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

    table = "repos_bak"
    
    # --------------------------------------------------------- #
    # 2. Calculate Derivative Variables:
    # --------------------------------------------------------- #

    #    - "library_to_total_loc_ratio"
    #    - "open_issues_to_total_issues_ratio"
    #    - "open_pulls_to_total_pulls_ratio"

    cur.execute(f"SELECT repo_id, self_written_loc, library_loc FROM {table}")
    locs_rows = cur.fetchall()

    library_to_total_loc_ratio_rows = []

    for row in locs_rows:
        library_to_total_loc_ratio_rows.append((row[0], row[2] / (row[1] + row[2])))

    # TODO: Add Column "library_to_total_loc_ratio" to the Table

    cur.execute(f"SELECT repo_id, open_issues, closed_issues FROM {table}")
    issues_rows = cur.fetchall()

    open_issues_to_total_issues_ratio_rows = []

    for row in issues_rows:
        if row[1] + row[2] == 0:  # check if total issues is zero, because of division by zero
            open_issues_to_total_issues_ratio_rows.append((row[0], row[1]))  # add open issues only
        else:
            open_issues_to_total_issues_ratio_rows.append((row[0], row[1] / (row[1] + row[2])))

    # TODO: Add Column "open_issues_to_total_issues_ratio" to the Table

    cur.execute(f"SELECT repo_id, open_pulls, closed_pulls FROM {table}")
    pulls_rows = cur.fetchall()

    open_pulls_to_total_pulls_ratio_rows = []

    for row in pulls_rows:
        if row[1] + row[2] == 0:
            open_pulls_to_total_pulls_ratio_rows.append((row[0], row[1]))
        else:
            open_pulls_to_total_pulls_ratio_rows.append((row[0], row[1] / (row[1] + row[2])))

    # TODO: Add Column "open_pulls_to_total_pulls_ratio" to the Table

    # TODO: Remove Column "notifications" from the Table

    # --------------------------------------------------------- #
    # 3. Normalize Dataset
    # --------------------------------------------------------- #

    # Columns: 

    # "repo_id" (Integer, PRIMARY KEY)
    # "open_issues" (Integer)
    # "closed_issues" (Integer)
    # "commits" (Integer)
    # "self_written_loc" (Integer)
    # "library_loc" (Integer)
    # "creation_date" (Varchar)
    # "stargazers" (Integer)
    # "latest_release" (Varchar)
    # "forks" (Integer)
    # "open_pulls" (Integer)
    # "closed_pulls" (Integer)
    # "releases" (Integer)
    # "network_events" (Integer)
    # "subscribers" (Integer)
    # "contributors" (Integer)
    # "watchers" (Integer)

    # Derivative Columns:
    #
    # "library_to_total_loc_ratio_rows" (Float)
    # "open_issues_to_total_issues_ratio_rows" (Float)
    # "open_pulls_to_total_pulls_ratio_rows" (Float)
    
    # TODO: Create a Table with the Normalized Values
    # TODO: Create a List of Tuples of each Column, and normalize them

    # --------------------------------------------------------- #
    # 4. Calculate Quality Measures (Pearson, Kendall, Spearman)
    # --------------------------------------------------------- #

    #   - Calculate Correlation Matrix (Visualize)
    #   - Hierarchical Clustering to 3 Clusters (Visualize)
    #   - Draw a Dendogram (Visualize)
    #   - Qualitative Reasoning for the Quality Score Names
    #   - Calculate Quality Scores
    #   - Calculate Quality Measures

    # --------------------------------------------------------- #
    # 5. New Correlation Matrix (Pearson, Kendall, Spearman)
    # --------------------------------------------------------- #

    #   - Pick up interesting correlations (Quality vs. Code Quantity)
    #   - Linear Correlation Calculation and Hypothesis Testing

    # Close the Cursor and Connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
