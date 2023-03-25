import analysis.analysis as a
import utils.utils as utils 

def main():
    # Read a File to a Variable.
    dataset_file = utils.read_csv_file("data/cleaned_dataset.csv")

    # Extract the Columns from the File.
    dataset_columns = utils.extract_columns(dataset_file, ["repository_name", "repository_url", "open_issue_count", "closed_issue_count", "commit_count", "open_closed_ratio", "stargazer_count", "creation_date", "latest_release", "original_codebase_size", "library_codebase_size", "library_to_original_ratio"])

    # utils.print_columns(dataset_columns)
    # utils.print_values(dataset_columns, "commit_count")

    # Normalize all the values to 0 - 1.
    normalized_dataset = a.normalize_dataset(dataset_columns)

    # TODO
    # qm = a.calculate_quality_measure(normalized_dataset)

    # Print the normalized values.
    utils.print_values(normalized_dataset, "stargazer_count")

    # TODO: Calculate Mean (QM) and save that to separate variable.

    # TODO: Calculate Spearman's Coefficient for: Ratio of Library Code : Open Closed Ratio
    
    # TODO: Calculate Spearman's Coefficient for: Ratio of Library Code : Stargazer Count
   
    # TODO: Calculate Spearman's Coefficient for: Ratio of Library Code : Commit Count
   
    # TODO: Calculate Spearman's Coefficient for: Ratio of Library Code : Creation Date
  
    # TODO: Calculate Spearman's Coefficient for: Ratio of Library Code : Latest Release
 
    # TODO: Calculate Spearman's Coefficient for: Ratio of Library Code : Average Quality Measure

    # TODO: Save Diagrams -> File.

    # TODO: Write also Pearson's Coefficient (?)

    x = {"a": 1, "b": 2, "c": 3}
    y = {"a": 4, "b": 5, "c": 6}
    rho, p = a.calculate_spearmanr(x, y)

    # print(rho)
    # print(p)


if __name__ == "__main__": 
    main()