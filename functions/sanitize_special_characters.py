import pandas as pd
import re

def sanitize_special_characters(df, exclude_cols=None):
    """
    Removes special characters from string fields.
    
    Rules:
    - exclude_cols: NOT sanitized at all (keep everything)
    - email columns: Keep @, ., _, - (for valid emails)
    - other columns: Remove ALL special chars including @
    - Also sanitizes column names (headers)
    """
    if exclude_cols is None:
        exclude_cols = []
    
    df = df.copy()
    
    # === FIX 1: Sanitize COLUMN NAMES (headers) ===
    # Remove ALL special chars from column names (no exceptions)
    new_columns = []
    for col in df.columns:
        cleaned = re.sub(r'[^a-zA-Z0-9\s_.\-]', '', str(col)).strip()
        new_columns.append(cleaned)
    df.columns = new_columns
    
    # === FIX 2: Sanitize CELL VALUES with smart rules ===
    
    def clean_value(value, is_email_col):
        """Clean a single value based on column type"""
        if pd.isna(value):
            return value
        
        text = str(value)
        
        # Skip pure numbers to avoid corrupting numeric data
        if text.replace('.', '').replace('-', '').isdigit():
            return value
        
        original = text
        
        if is_email_col:
            # Email columns: Keep @, ., _, - (for valid email format)
            # Remove: ! @ # $ % ^ & * ( ) + = { } [ ] | \ : ; " < > ? / ` ~ etc.
            # But KEEP: @ . _ -
            cleaned = re.sub(r'[^a-zA-Z0-9\s@._\-]', '', text).strip()
        else:
            # Non-email columns: Remove ALL special chars including @
            # Keep ONLY: letters, numbers, spaces, ., _, -
            cleaned = re.sub(r'[^a-zA-Z0-9\s._\-]', '', text).strip()
        
        return cleaned

    # Apply sanitization to each column
    for col in df.columns:
        if col in exclude_cols:
            # Skip excluded columns entirely (keep original values)
            continue
        
        # Check if this is an email column (by name)
        is_email_col = 'email' in col.lower()
        
        # Apply cleaning function
        df[col] = df[col].map(lambda v: clean_value(v, is_email_col))
    
    return df