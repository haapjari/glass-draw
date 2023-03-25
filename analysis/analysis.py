from scipy.stats import spearmanr
from typing import Dict
from datetime import datetime
from sklearn import preprocessing
import numpy as np

# Calculates Spearman's Rank Correlation Coefficient
# Returns Coefficient and P-Value
def calculate_spearmanr(x, y):
    x_values = list(x.values())
    y_values = list(y.values())
    rho, pvalue = spearmanr(x_values, y_values)
    return rho, pvalue

# https://www.digitalocean.com/community/tutorials/normalize-data-in-python
def normalize_dataset(dataset_columns: Dict[str, list]) -> Dict[str, list]:
    array = np.array(dataset_columns["creation_date"])

    normalized_array = preprocessing.normalize([array]) 
    print(normalized_array)

#    for column in dataset_columns:
        #if column == "repository_name" or column == "repository_url":
            #continue

        #if column == "creation_date" or column == "latest_release":
            #print("column is a datetype")
            #continue

        #print(column)
    