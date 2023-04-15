import numpy as np
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import kendalltau, pearsonr, spearmanr
from datetime import datetime
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.preprocessing import MinMaxScaler 


def normalize_values(data):
    ids, values = zip(*data)

    values_array = np.array(values).reshape(-1, 1)

    # Apply MinMaxScaler
    scaler = MinMaxScaler()
    normalized_values_array = scaler.fit_transform(values_array)

    # Combine the IDs and normalized values back into the desired format
    normalized_data = [(id, value[0]) for id, value in zip(ids, normalized_values_array)]

    return normalized_data


def calc_corr_matrix(df, method):
    n = len(df.columns)
    corr_matrix = pd.DataFrame(np.zeros((n, n)))
    for i in range(n):
        for j in range(n):
            if method == 'kendall':
                corr, _ = kendalltau(df.iloc[:, i], df.iloc[:, j])
            elif method == 'pearson':
                corr, _ = pearsonr(df.iloc[:, i], df.iloc[:, j])
            elif method == 'spearman':
                corr, _ = spearmanr(df.iloc[:, i], df.iloc[:, j])
            else:
                raise ValueError("Invalid correlation type. Use 'kendall', 'pearson', or 'spearman'.")
            corr_matrix.iat[i, j] = corr
    return corr_matrix


def correlation_heatmap(lists, corr_type):
    # Extract names and values from the input lists
    names, values = zip(*lists)

    # Create a DataFrame from the extracted values
    df = pd.DataFrame(list(zip(*values)), columns=names)

    # Calculate the correlation matrix based on the specified correlation type
    corr_matrix = calc_corr_matrix(df, corr_type)

    # Create a heatmap from the correlation matrix
    plt.figure(figsize=(10, 8))

    fig, ax = plt.subplots(figsize=(21, 17))

    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax, 
                annot_kws={"size": 16},
                xticklabels=list(map(str, names)),
                yticklabels=list(map(str, names)))

    ax.set_title("Correlation Matrix: " + corr_type, fontsize=20, loc='right', x=1.3, y=1.05)

    # Save the heatmap to the specified format
    if not os.path.exists("out"):
        os.makedirs("out")
    file_name = f"{datetime.now().isoformat()}_{corr_type}_heatmap.png"
    plt.savefig(f"out/{file_name}")

    # Return the correlation matrix
    return corr_matrix


def categorize_correlations(lists, corr_type):
    categories = {
        "Very Weak": [],
        "Weak": [],
        "Moderate": [],
        "Strong": [],
        "Very Strong": []
    }

    # Create a DataFrame from the lists
    data = pd.DataFrame(dict(lists))

    # Compute the correlation matrix
    corr_matrix = data.corr()

    variable_names = corr_matrix.columns

    for i in range(corr_matrix.shape[0]):
        for j in range(i+1, corr_matrix.shape[1]):
            corr = corr_matrix.iloc[i, j]
            if corr <= -0.7 or corr >= 0.7:
                categories["Very Strong"].append(((variable_names[i], variable_names[j]), corr))
            elif corr <= -0.5 or corr >= 0.5:
                categories["Strong"].append(((variable_names[i], variable_names[j]), corr))
            elif corr <= -0.3 or corr >= 0.3:
                categories["Moderate"].append(((variable_names[i], variable_names[j]), corr))
            elif corr <= -0.1 or corr >= 0.1:
                categories["Weak"].append(((variable_names[i], variable_names[j]), corr))
            else:
                categories["Very Weak"].append(((variable_names[i], variable_names[j]), corr))

    if not os.path.exists("out"):
        os.makedirs("out")

    with open("out" + "/" + datetime.now().isoformat() + "_" +  corr_type + "_" + "categories.txt", 'w') as f:
        for category, values in categories.items():
            f.write(f"{category}:\n")
            for value in values:
                f.write(f"- {value}\n")
            f.write("\n")

    return categories


def cluster_correlation_matrix(corr_matrix, corr_type, n_clusters=2, linkage_method='ward'):
    """
    Clusters a correlation matrix using hierarchical clustering.

    Parameters:
    corr_matrix (pandas.DataFrame): a correlation matrix as a pandas DataFrame
    n_clusters (int): the number of clusters to create
    linkage_method (str): the linkage method to use for clustering (default: 'ward')

    Returns:
    labels (numpy.array): an array of labels indicating which cluster each variable belongs to
    """

    # Convert correlation matrix to distance matrix
    dist_matrix = np.sqrt(1 - np.abs(corr_matrix))

    # Perform hierarchical clustering with specified linkage method
    Z = linkage(squareform(dist_matrix), method=linkage_method)

    # Assign labels to clusters
    labels = fcluster(Z, t=n_clusters, criterion='maxclust')

    if not os.path.exists("out"):
        os.makedirs("out")        

    with open("out" + "/" + datetime.now().isoformat() + "_" + corr_type + "_" + "cluster_output.txt", "w") as f:
        for i in range(1, n_clusters+1):
            f.write(f"Cluster {i}:\n")
            cluster_vars = [col for col, label in zip(corr_matrix.columns, labels) if label == i]
            for var in cluster_vars:
                f.write(f"- {var}\n")
            f.write("\n")

    return labels
