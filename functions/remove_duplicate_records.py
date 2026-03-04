import pandas as pd

def remove_duplicate_records(df):
    """Removes duplicate rows from DataFrame"""
    initial_count = len(df)
    df_cleaned = df.drop_duplicates()
    removed = initial_count - len(df_cleaned)
    if removed > 0:
        print(f"  ✓ Removed {removed} duplicate record(s)")
    return df_cleaned