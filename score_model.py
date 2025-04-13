
import pandas as pd

# Simulated scorecard table (replace with your real one if needed)
score_card = pd.DataFrame({
    'Variable': [
        'RevolvingUtilizationOfUnsecuredLines', 'RevolvingUtilizationOfUnsecuredLines',
        'NumberOfTimes90DaysLate', 'NumberOfTimes90DaysLate',
        'NumberOfTime30-59DaysPastDueNotWorse', 'NumberOfTime30-59DaysPastDueNotWorse',
        'age', 'age',
        'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfTime60-89DaysPastDueNotWorse'
    ],
    'Binning': [
        '(-inf, 0.1]', '(0.1, inf)',
        '(-inf, 0.5]', '(0.5, inf)',
        '(-inf, 0.5]', '(0.5, inf)',
        '(-inf, 45]', '(45, inf)',
        '(-inf, 0.5]', '(0.5, inf)'
    ],
    'Score': [50, 10, 30, -20, 25, -15, 20, 40, 20, -10]
})

# Base score (your model offset score, e.g. A = 600)
A = 600

# Convert bin strings to match range
def str_to_float(s):
    if s == '-inf':
        return -999999999.0
    elif s == 'inf':
        return 999999999.0
    else:
        return float(s)

def map_value_to_bin(value, feature_bins):
    for _, row in feature_bins.iterrows():
        bins = str(row['Binning'])
        left_open = bins[0] == '('
        right_open = bins[-1] == ')'
        lower, upper = bins[1:-1].split(',')

        lower = str_to_float(lower.strip())
        upper = str_to_float(upper.strip())

        if ((not left_open and value >= lower) or (left_open and value > lower)) and \
           ((not right_open and value <= upper) or (right_open and value < upper)):
            return row['Binning']
    return None

# Row-wise scoring
def map_to_score(row, score_card):
    score = 0
    for col in score_card['Variable'].unique():
        bins = score_card[score_card['Variable'] == col]
        value = row[col]
        bin_label = map_value_to_bin(value, bins)
        matched = bins[bins['Binning'] == bin_label]
        if not matched.empty:
            score += matched['Score'].values[0]
    return score

# Apply to DataFrame
def calculate_score_with_card(df, score_card, A):
    df = df.copy()
    df['score'] = df.apply(map_to_score, axis=1, score_card=score_card)
    df['score'] = df['score'] + A
    return df

# Decision logic
def score_to_decision(score):
    if score < 500:
        return 'Reject'
    elif score <= 650:
        return 'Manual Review'
    else:
        return 'Accept'
