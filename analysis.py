from scipy.stats import spearmanr

# Calculates Spearman's Rank Correlation Coefficient
# Returns Coefficient and P-Value
def calculate_spearmanr(x, y):
    x_values = list(x.values())
    y_values = list(y.values())
    rho, pvalue = spearmanr(x_values, y_values)
    return rho, pvalue
