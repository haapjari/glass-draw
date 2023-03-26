import pandas as pd


def calculate_quality_scores(data, type):
    if type == "pearson":
        # Define weights and signs for each input variable for maturity score
        maturity_latest_release_weight = 0.2   # Bigger value is better
        maturity_creation_date_weight = 0.2   # Smaller value is better
        maturity_open_closed_ratio_weight = 0.2   # Smaller value is better
        maturity_weights = {'latest_release': maturity_latest_release_weight,
                            'creation_date': maturity_creation_date_weight,
                            'open_closed_ratio': maturity_open_closed_ratio_weight}
        maturity_signs = {'latest_release': 1, 'creation_date': -1, 'open_closed_ratio': -1}

        # Define weights and signs for each input variable for activity score
        activity_commit_count_weight = 0.2    # Bigger value is better
        activity_stargazer_count_weight = 0.2   # Bigger value is better
        activity_weights = {'commit_count': activity_commit_count_weight,
                            'stargazer_count': activity_stargazer_count_weight}
        activity_signs = {'commit_count': 1, 'stargazer_count': 1}

        # Compute the Maturity Score as a weighted average of the input variables
        maturity_score = 0
        for var in maturity_weights:
            maturity_score += (maturity_signs[var] * maturity_weights[var] * data[var])
        maturity_score = (maturity_score - maturity_score.min()) / (maturity_score.max() - maturity_score.min())

        # Compute the Activity Score as a weighted average of the input variables
        activity_score = 0
        for var in activity_weights:
            activity_score += (activity_signs[var] * activity_weights[var] * data[var])
        activity_score = (activity_score - activity_score.min()) / (activity_score.max() - activity_score.min())

        # Compute the Quality Measure as a weighted average of the Maturity Score and Activity Score
        maturity_weight = 0.6
        activity_weight = 0.4
        quality_measure = (maturity_weight * maturity_score) + (activity_weight * activity_score)

        # Add the Maturity Score, Activity Score, and Quality Measure to the input DataFrame
        data['maturity_score'] = maturity_score
        data['activity_score'] = activity_score
        data['quality_measure'] = quality_measure

        return data
