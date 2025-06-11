# database/insert_data.py
from oracle_connection import get_connection
import pandas as pd
import datetime
import os


def insert_data():
    #df = pd.read_csv("Data/all_bank_with_sentiment.csv", parse_dates=["date"])
    file_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'all_banks_with_sentiment.csv')
    df = pd.read_csv(file_path, parse_dates=["date"])
    
    # Drop rows with any missing critical fields
    df = df.dropna(subset=['bank_name', 'date', 'rating', 'cleaned_text', 'sentiment_label', 'sentiment_score'])

    # Coerce rating and sentiment_score to numeric, dropping anything invalid
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce')
    df = df.dropna(subset=['rating', 'sentiment_score'])
    
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # Insert banks
    for bank in df['bank_name'].unique():
        cursor.execute("""
        MERGE INTO banks b
        USING (SELECT :1 AS bank_name FROM dual) d
        ON (b.bank_name = d.bank_name)
        WHEN NOT MATCHED THEN INSERT (bank_name) VALUES (:1)
        """, [bank])
    conn.commit()

    # Insert reviews
    for _, row in df.iterrows():
        cursor.execute("SELECT bank_id FROM banks WHERE bank_name = :1", [row['bank_name']])
        bank_id = cursor.fetchone()[0]

        cursor.execute("""
        INSERT INTO reviews (bank_id, review_date, rating, cleaned_text, sentiment_label, sentiment_score)
        VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6)
        """, (
            bank_id,
            row['date'].strftime('%Y-%m-%d'),
            int(row['rating']),
            row['cleaned_text'],
            row['sentiment_label'],
            float(row['sentiment_score'])
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted successfully.")

if __name__ == "__main__":
    insert_data()