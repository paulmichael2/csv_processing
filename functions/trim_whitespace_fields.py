import pandas as pd

def trim_whitespace_fields(df):
    """Trims leading/trailing whitespace from all string fields"""
    for col in df.columns:
        # Check for any text-like dtype
        if df[col].dtype == 'object' or str(df[col].dtype) in ['string', 'str']:
            df[col] = df[col].astype(str).str.strip()
    print("  ✓ Trimmed whitespace from string fields")
    return df