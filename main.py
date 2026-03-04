import os
import pandas as pd
import re

# =============================================================================
# ALL 5 FUNCTIONS DEFINED INLINE - NO IMPORTS NEEDED
# =============================================================================

def remove_duplicate_records(df):
    """Removes duplicate rows"""
    initial = len(df)
    df = df.drop_duplicates()
    print(f"  Removed {initial - len(df)} duplicates")
    return df

def trim_whitespace_fields(df):
    """Trims whitespace from string columns"""
    for col in df.columns:
        if df[col].dtype == 'object' or str(df[col].dtype) == 'string':
            df[col] = df[col].astype(str).str.strip()
    print("  Trimmed whitespace")
    return df

def fill_missing_values(df):
    """Fills missing values: numeric=mean, text=mode"""
    for col in df.columns:
        if df[col].isna().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                mode = df[col].mode()
                df[col] = df[col].fillna(mode[0] if len(mode) > 0 else 'Unknown')
    print("  Filled missing values")
    return df

def standardize_date_formats(df):
    """Standardizes date columns to YYYY-MM-DD"""
    date_keywords = ['date', 'time', 'join', 'created', 'updated']
    for col in df.columns:
        if any(kw in col.lower() for kw in date_keywords):
            try:
                parsed = pd.to_datetime(df[col], errors='coerce')
                if parsed.notna().any():
                    df[col] = parsed.dt.strftime('%Y-%m-%d')
            except:
                pass
    print("  Standardized dates")
    return df

def sanitize_special_characters(df):
    """
    FINAL: Removes ALL special characters from values AND column names.
    Keeps: letters, numbers, spaces, @, ., _, -
    """
    print(f"\n🚀 [SANITIZE] Running...")
    
    # Fix 1: Sanitize COLUMN NAMES
    new_cols = []
    for col in df.columns:
        cleaned = re.sub(r'[^a-zA-Z0-9\s@._-]', '', str(col)).strip()
        new_cols.append(cleaned)
        if col != cleaned:
            print(f"  ✂️ Header: '{col}' → '{cleaned}'")
    df.columns = new_cols
    
    # Fix 2: Sanitize CELL VALUES
    KEEP_PATTERN = r'[^a-zA-Z0-9\s@._-]'
    
    def clean_val(v):
        if pd.isna(v): return v
        txt = str(v)
        # Skip pure numbers
        if txt.replace('.','').replace('-','').isdigit():
            return v
        original = txt
        cleaned = re.sub(KEEP_PATTERN, '', txt).strip()
        if original != cleaned:
            print(f"    ✂️ '{original}' → '{cleaned}'")
        return cleaned
    
    # Apply to ALL columns
    for col in df.columns:
        df[col] = df[col].map(clean_val)
    
    print(f"✅ [SANITIZE] Done\n")
    return df

# =============================================================================
# MAIN PROCESSING LOGIC
# =============================================================================

def process_csv_file(input_path, output_path):
    print(f"\n{'='*60}")
    print(f"Processing: {input_path}")
    print(f"{'='*60}")
    
    # Read ONCE
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} rows, columns: {list(df.columns)}")
    
    # Chain ALL functions (passing DataFrame)
    print("\n[1/5] Removing duplicates...")
    df = remove_duplicate_records(df)
    
    print("[2/5] Trimming whitespace...")
    df = trim_whitespace_fields(df)
    
    print("[3/5] Filling missing values...")
    df = fill_missing_values(df)
    
    print("[4/5] Standardizing dates...")
    df = standardize_date_formats(df)
    
    print("[5/5] Sanitizing special characters...")
    df = sanitize_special_characters(df)  # ← This is the fixed one!
    
    # Clean up float columns
    for col in df.select_dtypes(include=['float64']).columns:
        if df[col].notna().all() and (df[col] % 1 == 0).all():
            df[col] = df[col].astype(int)
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved: {output_path}")
    print(f"✓ Final: {len(df)} rows")
    print(f"{'='*60}\n")
    
    return df

def process_all_files():
    input_dir = 'input'
    output_dir = 'output'
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    if not csv_files:
        print("❌ No CSV files in input/")
        return
    
    print(f"Found {len(csv_files)} file(s)\n")
    
    for filename in csv_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"processed_{filename}")
        try:
            process_csv_file(input_path, output_path)
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✅ All done!")

if __name__ == "__main__":
    process_all_files()