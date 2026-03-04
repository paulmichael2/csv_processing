import pandas as pd

def standardize_date_formats(df):
    """Standardizes date columns to YYYY-MM-DD format"""
    date_keywords = ['date', 'time', 'join', 'created', 'updated', 'birth']
    standardized = []
    
    for col in df.columns:
        # Check if column name suggests it's a date
        is_date_col = any(kw in col.lower() for kw in date_keywords)
        
        if is_date_col:
            try:
                parsed = pd.to_datetime(df[col], errors='coerce', dayfirst=False)
                if parsed.notna().any():
                    df[col] = parsed.dt.strftime('%Y-%m-%d')
                    standardized.append(col)
            except:
                pass
    
    if standardized:
        print(f"  ✓ Standardized dates in: {standardized}")
    return df