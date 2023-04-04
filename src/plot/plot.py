from datetime import datetime
import csv
import chardet
import sys
import io
import pandas as pd
from collections import OrderedDict
import numpy
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import pearsonr, spearmanr, kendalltau
import os
import seaborn as sns
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram

mpl.use('agg')

# Calculate and draw a plot for the Library to Original Ratio and Quality Measure.
def plot(analysis_method, dataset, x_type, y_type): 
    """
    Plots a scatter plot of the data points with a line of best fit, using the specified analysis method.

    Parameters:
    analysis_method (str): The statistical analysis method to be used. Must be "pearsonr" or "spearmanr".
    repos (List): A list of repositories.
    x_type (str): The type of data to be plotted on the x-axis.
    y_type (str): The type of data to be plotted on the y-axis.
    x_min (float): The minimum value for the x-axis.
    x_max (float): The maximum value for the x-axis.
    y_min (float): The minimum value for the y-axis.
    y_max (float): The maximum value for the y-axis.

    Returns:
    None

    """

    x = numpy.ravel(dataset[x_type])
    y = numpy.ravel(dataset[y_type])

    coefficient = None
    p = None

    if analysis_method == "pearson":
        coefficient, p = pearsonr(x, y) 
        
        print("Pearson's Correlation Coefficient: {} and Probability Value: {}".format(coefficient, p))

    if analysis_method == "spearman":
        coefficient, p = spearmanr(x, y) 
        
        print("Spearman's Correlation Coefficient: {} and Probability Value: {}".format(coefficient, p))
    
    if analysis_method == "kendall":
        coefficient, p = kendalltau(x, y) 
        
        print("Kendall's Correlation Coefficient: {} and Probability Value: {}".format(coefficient, p))
    
        # Calculate coefficients, and function for the line of best fit.
    data = numpy.polyfit(x, y, 1)
    polynomial = numpy.poly1d(data)

    # Plot the Values
    plt.scatter(x, y,color='black', s=0.5, alpha=1, marker="o", linewidth=0, label="Data Points", zorder=1, edgecolors=None, facecolors=None, antialiased=True, rasterized=None, norm=None, vmin=None, vmax=None, data=None)
    plt.plot(x, polynomial(x),color='black', linewidth=0.1, label="Linear Regression", zorder=1, antialiased=True, rasterized=True, data=None)
    plt.xlabel(x_type)
    plt.ylabel(y_type)
    plt.autoscale(enable=True, axis='both', tight=None)

    legend_coefficient = plt.legend(["r = " + str(coefficient)], loc='upper right', bbox_to_anchor=(1.0, 1.0))

    if analysis_method == "pearson":
        legend_coefficient.set_title("Pearson's Correlation Coefficient")
    
    if analysis_method == "spearman":
        legend_coefficient.set_title("Spearman's Correlation Coefficient")
    
    if analysis_method == "kendall":
        legend_coefficient.set_title("'s Correlation Coefficient")

    legend_coefficient.get_title().set_fontsize('small')
    legend_coefficient.get_title().set_fontweight('bold')
    
    legend_p = plt.legend(["p = " + str(p)], loc='upper right', bbox_to_anchor=(1.0, 0.85))
    legend_p.set_title("Probability Value")
    legend_p.get_title().set_fontsize('small')
    legend_p.get_title().set_fontweight('bold')

    plt.gca().add_artist(legend_coefficient)
    plt.gca().add_artist(legend_p)

    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.05, color='grey', alpha=0.75)

    now = datetime.now()
    iso_date_string = now.isoformat()

    ## Limiting the x -axis to make the plot more readable.
    plt.axis([min(x), max(x), min(y), max(y)])

    if not os.path.exists("out"):
        os.makedirs("out")

    plt.savefig("out/"+iso_date_string + "_" + analysis_method + "_" + x_type + "_to_" + y_type +'.png', dpi=300, bbox_inches='tight', pad_inches=0.1)


def heatmap(dataset, corr_type, exclude_columns):
    """
    Generates a heatmap to display the correlation between variables in a given dataset.

    Parameters:
        dataset (dict): A dictionary containing numerical data in the form of numpy arrays.

    Returns:
        None.

    Side effects:
        - Deletes the "repository_name" and "repository_url" columns from the dataset.
        - Reshapes each array in the dataset to be one-dimensional.
        - Generates a correlation matrix for the dataset using pandas.
        - Displays the correlation matrix as a heatmap using seaborn.
        - Saves the resulting plot to a file in a subdirectory called "out" with a filename that includes the
          current date and time in ISO format (e.g., "2022-12-31T23:59:59.999999_correlation_matrix.png").
    """
    # Delete Columns, that are not included in the heatmap.
    #for column in exclude_columns:
        #del dataset[column]

    # Convert Arrays in Dictionary to be One-Dimensional
    for key in dataset.keys():
        dataset[key] = numpy.reshape(dataset[key], -1)

    df = pd.DataFrame.from_dict(dataset)

    corr_matrix = df.corr(corr_type)

    fig, ax = plt.subplots(figsize=(21, 17))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax, fmt=".2f", 
                annot_kws={"size": 16})

    ax.set_title("Correlation Matrix: " + corr_type, fontsize=20, loc='right', x=1.3, y=1.05)

    if not os.path.exists("out"):
        os.makedirs("out")

    now = datetime.now()
    iso_date_string = now.isoformat()

    # Save the plot to a file
    plt.savefig('out' + '/' + iso_date_string + "_" + corr_type + "_" + 'correlation_matrix.png')


def correlation_matrix(dataset, corr_type, exclude_columns):
    # Delete Columns, that are not included in the heatmap.
    for column in exclude_columns:
        del dataset[column]

    # Convert Arrays in Dictionary to be One-Dimensional
    for key in dataset.keys():
        dataset[key] = numpy.reshape(dataset[key], -1)

    df = pd.DataFrame.from_dict(dataset)

    corr_matrix = df.corr(corr_type)

    return corr_matrix, df.columns

     

def visualize_categories(categories, corr_type, chart_type):
    if chart_type == "bar":
        x_labels = list(categories.keys())
        y_values = [len(categories[k]) for k in x_labels]
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(x_labels, y_values, color=['#cccccc', '#cccccc', '#cccccc', '#cccccc', '#cccccc'])
        ax.set_title('Correlation Categories')
        ax.set_xlabel('Category')
        ax.set_ylabel('Number of Correlations')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('correlation_categories.png')
    
        if not os.path.exists("out"):
            os.makedirs("out")

        # Save the plot to a file
        plt.savefig('out' + '/' + datetime.now().isoformat() + "_" + corr_type + "_" + 'correlation_categories' + "_" + chart_type + '.png')

    if chart_type == "bubble":
        fig, ax = plt.subplots()
        ax.set_xlabel('Variable 1')
        ax.set_ylabel('Variable 2')
        ax.set_title('Correlation Coefficient Bubble Chart')

        for category, pairs in categories.items():
            for pair in pairs:
                x, y = pair[0]
                size = abs(pair[1]) * 100
                color = 'red' if pair[1] < 0 else 'green'
                ax.scatter(x, y, s=size, c=color, alpha=0.5, label=category)

        ax.legend(loc='best', title='Category')
        fig.tight_layout()

        if not os.path.exists("out"):
            os.makedirs("out")        

        plt.savefig('out' + '/' + datetime.now().isoformat() + "_" + corr_type + "_" + 'correlation_categories' + "_" + chart_type + '.png')


def visualize_dendrogram(corr_matrix, corr_type, linkage_method='ward'):
    """
    Visualizes a dendrogram of a correlation matrix using hierarchical clustering.

    Parameters:
    corr_matrix (pandas.DataFrame): a correlation matrix as a pandas DataFrame
    linkage_method (str): the linkage method to use for clustering (default: 'ward')

    Returns:
    None
    """

    # Convert correlation matrix to distance matrix
    dist_matrix = numpy.sqrt(1 - numpy.abs(corr_matrix))

    # Perform hierarchical clustering
    Z = linkage(squareform(dist_matrix), method='ward')

    # Plot dendrogram with variable names
    plt.figure(figsize=(10, 8))
    dendrogram(Z, labels=corr_matrix.columns, orientation='right', leaf_font_size=7)

    # Set plot parameters
    plt.xlabel('Distance')

    if not os.path.exists("out"):
        os.makedirs("out")        

    plt.savefig('out' + '/' + datetime.now().isoformat() + "_" + corr_type + "_" + 'dendogram.png')
