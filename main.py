import analysis.analysis as a
import utils.utils as utils 
from models.repository import extract_repositories
from plot.plot import plot

def main():
    # Read a File to a Variable.
    dataset_file = utils.read_csv_file("data/cleaned_dataset.csv")

    # Extract the Columns from the File.
    dataset_columns = utils.extract_columns(dataset_file, ["repository_name", "repository_url", "open_issue_count", "closed_issue_count", "commit_count", "open_closed_ratio", "stargazer_count", "creation_date", "latest_release", "original_codebase_size", "library_codebase_size", "library_to_original_ratio"])

    # Normalize all the values to 0 - 1.
    normalized_dataset = a.normalize_dataset(dataset_columns)

    # Adjust dataset, so all the normalized values will be
    # handled similarly, bigger is better and smaller is worse.
    adjusted_dataset = a.adjust_normalized_columns(normalized_dataset)

    # Extract Repository objects from the data, which includes fields
    # and they have normalized values of "adjusted_dataset".
    # Append the list with "quality_measure" values.
    # TODO: Rethink the Concept of the Quality Measure, is it actually usable 
    # here.
    repos = a.calculate_quality_measures(extract_repositories(adjusted_dataset))

    valid_columns = ["open_issue_count", "closed_issue_count", "commit_count", "open_closed_ratio", "stargazer_count", "creation_date", "latest_release", "original_codebase_size", "library_codebase_size", "library_to_original_ratio", "quality_measure"]

    while True:
        correlation_type = input("Enter correlation type (pearsonr or spearmanr) (or 'quit' to exit): ")
        if correlation_type.lower() == "quit":
            break
        if correlation_type.lower() not in ["pearsonr", "spearmanr"]:
            print("Error: Invalid correlation type.")
            continue

        print(f"Valid columns: {', '.join(valid_columns)}")

        x = input("Enter x parameter for plot (or 'quit' to exit): ")
        if x.lower() == "quit":
            break
        elif x not in valid_columns:
            print(f"Error: {x} is not a valid column.")
            continue

        y = input("Enter y parameter for plot (or 'quit' to exit): ")
        if y.lower() == "quit":
            break
        elif y not in valid_columns:
            print(f"Error: {y} is not a valid column.")
            continue
        
        plot(correlation_type, repos, x, y)


if __name__ == "__main__": 
    main()