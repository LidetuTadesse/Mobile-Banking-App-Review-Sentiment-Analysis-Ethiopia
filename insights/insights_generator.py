# # insights/insights_generator.py
# import pandas as pd
# from collections import Counter

# def extract_drivers_pain_points(df):
#     drivers, pains = {}, {}

#     for bank in df['bank_name'].unique():
#         sub_df = df[df['bank_name'] == bank]
#         drivers[bank] = sub_df[sub_df['sentiment_label'] == 'positive']['cleaned_text'].sample(3).tolist()
#         pains[bank] = sub_df[sub_df['sentiment_label'] == 'negative']['cleaned_text'].sample(3).tolist()

#     return drivers, pains

# def compare_banks(df):
#     comparison = df.groupby('bank_name').agg({
#         'rating': ['mean'],
#         'sentiment_score': ['mean']
#     }).round(2)
#     return comparison

import pandas as pd
from collections import Counter

def extract_drivers_pain_points(df):
    drivers, pains = {}, {}

    for bank in df['bank_name'].unique():
        sub_df = df[df['bank_name'] == bank]

        # Normalize sentiment labels just in case
        sub_df['sentiment_label'] = sub_df['sentiment_label'].str.upper()

        # Extract positive reviews
        pos_reviews = sub_df[sub_df['sentiment_label'] == 'POSITIVE']['cleaned_text']
        if len(pos_reviews) >= 3:
            drivers[bank] = pos_reviews.sample(3).tolist()
        else:
            drivers[bank] = pos_reviews.sample(len(pos_reviews)).tolist() if not pos_reviews.empty else []

        # Extract negative reviews
        neg_reviews = sub_df[sub_df['sentiment_label'] == 'NEGATIVE']['cleaned_text']
        if len(neg_reviews) >= 3:
            pains[bank] = neg_reviews.sample(3).tolist()
        else:
            pains[bank] = neg_reviews.sample(len(neg_reviews)).tolist() if not neg_reviews.empty else []

    return drivers, pains

def compare_banks(df):
    comparison = df.groupby('bank_name').agg({
        'rating': ['mean'],
        'sentiment_score': ['mean']
    }).round(2)
    return comparison
