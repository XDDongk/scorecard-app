
import pandas as pd

# Real scorecard table
score_card = pd.DataFrame({
    'Variable': [
        'NumberOfTime30-59DaysPastDueNotWorse'] * 10 +
        ['NumberOfTime60-89DaysPastDueNotWorse'] * 10 +
        ['NumberOfTimes90DaysLate'] * 10 +
        ['RevolvingUtilizationOfUnsecuredLines'] * 5 +
        ['age'] * 6,
    'Binning': [
        '(-inf, 1.0]', '(1.0, 2.0]', '(7.0, 8.0]', '(8.0, 9.0]', '(2.0, 3.0]',
        '(3.0, 4.0]', '(4.0, 5.0]', '(6.0, 7.0]', '(5.0, 6.0]', '(9.0, inf]',
        '(8.0, 9.0]', '(-inf, 1.0]', '(7.0, 8.0]', '(6.0, 7.0]', '(1.0, 2.0]',
        '(2.0, 3.0]', '(3.0, 4.0]', '(4.0, 5.0]', '(5.0, 6.0]', '(9.0, inf]',
        '(-inf, 1.0]', '(1.0, 2.0]', '(9.0, inf]', '(2.0, 3.0]', '(5.0, 6.0]',
        '(4.0, 5.0]', '(3.0, 4.0]', '(7.0, 8.0]', '(8.0, 9.0]', '(6.0, 7.0]',
        '(-0.00099163, 0.0314]', '(0.0314, 0.107]', '(0.107, 0.31]',
        '(0.31, 0.736]', '(0.736, 11.385]',
        '(70.0, inf]', '(60.0, 70.0]', '(50.0, 60.0]', '(40.0, 50.0]',
        '(25.0, 40.0]', '(-inf, 25.0]'
    ],
    'Score': [
        12, -81, -86, -96, -102, -118, -123, -135, -138, -175,
        89, 3, -101, -105, -107, -116, -125, -128, -149, -190,
        8, -129, -137, -144, -144, -154, -164, -169, -178, -196,
        97, 81, 45, -8, -71,
        40, 24, 3, -8, -16, -1
    ]
})

A = 600

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

def calculate_score_with_card(df, score_card, A):
    df = df.copy()
    df['score'] = df.apply(map_to_score, axis=1, score_card=score_card)
    df['score'] = df['score'] + A
    return df

def score_to_decision(score):
    if score < 530:
        return 'Reject'
    elif score <= 620:
        return 'Manual Review'
    else:
        return 'Accept'
}
