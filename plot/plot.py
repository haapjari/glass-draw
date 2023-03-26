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
from scipy.stats import pearsonr, spearmanr
import os

mpl.use('agg')

# Calculate and draw a plot for the Library to Original Ratio and Quality Measure.
def plot(analysis_method, repos, x_type, y_type): 
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
    # Populate x and y axis lists.
    x = []
    y = []
    for repo in repos:
        if hasattr(repo, x_type):
            x.append(getattr(repo, x_type))
        
        if hasattr(repo, y_type):
            y.append(getattr(repo, y_type))

    coefficient = None
    p = None

    if analysis_method == "pearsonr":
        coefficient, p = pearsonr(x, y) 
        
        print("Pearson's Correlation Coefficient: {} and Probability Value: {}".format(coefficient, p))

    if analysis_method == "spearmanr":
        coefficient, p = spearmanr(x, y) 
        
        print("Spearman's Correlation Coefficient: {} and Probability Value: {}".format(coefficient, p))

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

    if analysis_method == "pearsonr":
        legend_coefficient.set_title("Pearson's Correlation Coefficient")
    
    if analysis_method == "spearmanr":
        legend_coefficient.set_title("Spearman's Correlation Coefficient")

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