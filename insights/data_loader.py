# # insights/data_loader.py
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from database.oracle_connection import get_connection
# import pandas as pd

# def load_reviews():
#     conn = get_connection()
#     if not conn:
#         raise Exception("Connection failed")

#     query = """
#     SELECT r.review_id, r.review_date, r.rating, r.cleaned_text, 
#            r.sentiment_label, r.sentiment_score, b.bank_name
#     FROM reviews r
#     JOIN banks b ON r.bank_id = b.bank_id
#     """
    
#     df = pd.read_sql(query, con=conn)
#     conn.close()

#     # Normalize column names to lowercase
#     df.columns = df.columns.str.lower()

#     # Convert Oracle CLOBs to string if 'cleaned_text' exists
#     if 'cleaned_text' in df.columns:
#         df['cleaned_text'] = df['cleaned_text'].apply(lambda x: str(x.read()) if hasattr(x, 'read') else str(x))
#     return df

# insights/data_loader.py

# insights/data_loader.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from database.oracle_connection import get_connection

def load_reviews():
    conn = get_connection()
    if not conn:
        raise Exception("Database connection failed.")

    query = """
    SELECT r.review_id, r.review_date, r.rating, r.cleaned_text, 
           r.sentiment_label, r.sentiment_score, b.bank_name
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query)

        # Get column names
        columns = [col[0].lower() for col in cursor.description]

        rows = []
        for row in cursor.fetchall():
            row_dict = {}
            for col, val in zip(columns, row):
                if hasattr(val, 'read'):  # For CLOBs
                    row_dict[col] = val.read()
                else:
                    row_dict[col] = val
            rows.append(row_dict)

        df = pd.DataFrame(rows)

        return df

    finally:
        conn.close()
