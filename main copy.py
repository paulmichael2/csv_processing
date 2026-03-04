import os
import pandas as pd

# Import functions with CORRECT filenames (NO func_ prefix)
from functions.remove_duplicate_records import remove_duplicate_records
from functions.trim_whitespace_fields import trim_whitespace_fields
from functions.fill_missing_values import fill_missing_values
from functions.standardize_date_formats import standardize_date_formats
from functions.sanitize_special_characters import sanitize_special_characters


def process_csv_file(input_path, output_path):
    """Process a single CSV file through all 5 cleaning functions."""
    print(f"\n{'='*60}")
    print(f"Processing: {input_path}")
    print(f"{'='*60}")
    
    # 🔑 READ THE FILE ONCE AT THE START
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} rows")
    
    # 🔑 CHAIN FUNCTIONS: Pass DataFrame, NOT file path
    print("\n[1/5] Removing duplicates...")
    df = remove_duplicate_records(df)
    
    print("[2/5] Trimming whitespace...")
    df = trim_whitespace_fields(df)
    
    print("[3/5] Filling missing values...")
    df = fill_missing_values(df)
    
    print("[4/5] Standardizing date formats...")
    df = standardize_date_formats(df)
    
    print("[5/5] Sanitizing special characters...")
    df = sanitize_special_characters(df)  # No exclusions needed with fixed regex
    
    # Convert float columns back to int if possible (cleaner output)
    for col in df.select_dtypes(include=['float64']).columns:
        if df[col].notna().all() and (df[col] % 1 == 0).all():
            df[col] = df[col].astype(int)
    
    # Save the processed file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved: {output_path}")
    print(f"✓ Final: {len(df)} rows")
    print(f"{'='*60}\n")
    
    return df


def process_all_files():
    """Process all CSV files in the input directory."""
    input_dir = 'input'
    output_dir = 'output'
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files found in input directory!")
        return
    
    print(f"Found {len(csv_files)} CSV file(s) to process\n")
    
    for filename in csv_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"processed_{filename}")
        
        try:
            process_csv_file(input_path, output_path)
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("✅ All files processed successfully!")
    print(f"{'='*60}")


if __name__ == "__main__":
    process_all_files()