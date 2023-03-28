import os
import csv
from github import Github
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()


# TODO: Untested
def extend_dataset(input_file, output_file, additional_fields):
    # Read in the data from the input CSV file
    with open(input_file) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    # Create a PyGithub object with the API token from the .env file
    g = Github(os.environ["GITHUB_API_TOKEN"])

    # Loop over each repository in the data and fetch the additional information from the API
    for row in data:
        # Extract the repository owner and name from the URL in the second column
        owner, name = row[1].split("/")[-2:]
        repo = g.get_repo(f"{owner}/{name}")

        # Add the additional information to the row
        row.extend([getattr(repo, field, "") for field in additional_fields])

    # Write out the extended data to a new CSV file
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header + additional_fields)
        writer.writerows(data)


def test_github_api():
    g = Github(os.environ["GITHUB_API_TOKEN"])

    # Replace REPO_OWNER and REPO_NAME with the actual repository owner and name
    repo = g.get_repo("kubernetes/kubernetes")

    # Print out the available fields for the repository
    print("Available fields for the repository:")
    for attr in dir(repo):
        if not attr.startswith("_"):
            print(attr)


# TODO: Untested
def query_latest_commits():
    # Create a PyGithub object with the API token from the .env file
    g = Github(os.environ["GITHUB_API_TOKEN"])

    # Get the kubernetes/kubernetes repository
    repo = g.get_repo("kubernetes/kubernetes")

    # Get the latest 10 commits for the repository
    commits = repo.get_commits()[0:10]

    # Loop over the commits and print out their dates and total number of changes
    for commit in commits:
        # Get the commit object for this commit
        full_commit = repo.get_commit(commit.sha)

        # Calculate the total number of changes
        total_changes = full_commit.stats.additions + full_commit.stats.deletions

        # Print out the date and total number of changes
        print(f"Date: {full_commit.commit.author.date}")
        print(f"Changes: {total_changes}")


# TODO: Untested
def get_commit_info(repo_name, owner):
    # Create a PyGithub object with the API token from the .env file
    g = Github(os.environ["GITHUB_API_TOKEN"])

    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Initialize the date range for the commits to the creation date of the repository and the current date
    since_date = repo.created_at
    until_date = datetime.now(timezone.utc)

    # Initialize the dictionary of commit hashes mapped to their date and total number of changes
    commit_info = {}

    # Loop over the pages of commits and add their date and total number of changes to the dictionary
    while True:
        commits = repo.get_commits(since=since_date, until=until_date)
        for commit in commits:
            full_commit = repo.get_commit(commit.sha)
            total_changes = full_commit.stats.additions + full_commit.stats.deletions
            commit_info[commit.sha] = (full_commit.commit.author.date, total_changes)
        if len(commits) == 0:
            break
        since_date = commits[-1].commit.author.date

    # Return the dictionary of commit hashes mapped to their date and total number of changes
    return commit_info