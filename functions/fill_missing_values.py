import pandas as pd

def fill_missing_values(df):
    """Fills missing values: numeric=mean, text=mode"""
    missing_before = df.isnull().sum().sum()
    
    for col in df.columns:
        if df[col].isna().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                mode = df[col].mode()
                fill_value = mode[0] if len(mode) > 0 else 'Unknown'
                df[col] = df[col].fillna(fill_value)
    
    missing_after = df.isnull().sum().sum()
    print(f"  ✓ Filled {missing_before - missing_after} missing value(s)")
    return df