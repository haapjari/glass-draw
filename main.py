import analysis as a
import utils 

def main():
    # Read a File to a Variable.
    dataset_file = utils.read_csv_file("data/dataset.csv")

    # TODO: Extract Columns from a Variable to Dictionaries.
    # utils.extract_columns

    # TODO: Normalize all the values to 0 - 5.

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

    print(rho)
    print(p)


if __name__ == "__main__": 
    main()