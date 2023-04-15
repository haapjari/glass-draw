import pandas as pd


# The "health_score" value calculated by the refactored function is essentially a weighted mean of the signals in the input dictionary. The function calculates the mean of each signal (by summing up the values in the list and dividing by the number of elements) and then adjusts the mean value with a predefined weight and sign. The weighted means of all signals are then summed up to produce the final health score.


def calculate_qs_pearson_health(data):
    health_weights = {
        'open_to_total_pulls_ratio': 0.2,
        'open_to_total_issues_ratio': 0.2,
        'latest_release': 0.2,
        'creation_date': 0.2,
        'releases': 0.2
    }
    health_signs = {
        'open_to_total_pulls_ratio': -1,
        'open_to_total_issues_ratio': -1,
        'latest_release': 1,
        'creation_date': -1,
        'releases': 1
    }

    n = len(data['open_to_total_pulls_ratio'])
    health_scores = [0] * n

    for var in health_weights:
        for i in range(n):
            health_scores[i] += (health_signs[var] * health_weights[var] * data[var][i])

    return health_scores


def calculate_qs_pearson_engagement(data):
    weights = {
        'contributors': 0.14285714285714285,
        'commits': 0.14285714285714285,
        'network_events': 0.14285714285714285,
        'forks': 0.14285714285714285,
        'subscribers': 0.14285714285714285,
        'watchers': 0.14285714285714285,
        'stargazers': 0.14285714285714285
    }
    signs = {
        'contributors': 1,
        'commits': 1,
        'network_events': 1,
        'forks': 1,
        'subscribers': 1,
        'watchers': 1,
        'stargazers': 1
    }

    n = len(data['contributors'])
    scores = [0] * n

    for var in weights:
        for i in range(n):
            scores[i] += (signs[var] * weights[var] * data[var][i])

    return scores
