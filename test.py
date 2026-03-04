import pandas as pd
import re

def sanitize_special_characters(df, exclude_cols=None):
    if exclude_cols is None:
        exclude_cols = []
    df = df.copy()
    KEEP_PATTERN = r'[^a-zA-Z0-9\s@._-]'
    
    def clean_value(value):
        if pd.isna(value):
            return value
        text = str(value)
        if not any(c.isalpha() for c in text):
            return value
        original = text
        cleaned = re.sub(KEEP_PATTERN, '', text).strip()
        if original != cleaned:
            print(f"  ✂️ '{original}' → '{cleaned}'")
        return cleaned

    for col in df.columns:
        if col not in exclude_cols:
            df[col] = df[col].map(clean_value)
    return df

# Test with YOUR exact data
test = pd.DataFrame({
    'name': ['Jack!!!&Williams', 'Leo Gar @@@@@@@cia', '  John Doe  '],
    'email': ['bob!!!.johnson@email.com', '!!!b.johnson@email.com', 'john.doe@email.com'],
    'department': ['Engineering!!!', '!!!!!!Engineering', 'Sales']
})

print("=== BEFORE ===")
print(test)
print("\n=== dtypes ===")
print(test.dtypes)
print("\n=== AFTER ===")
result = sanitize_special_characters(test)
print(result)
print("\n=== Verification ===")
for col in result.columns:
    has_bad = result[col].astype(str).str.contains(r'[!@#$%^&*]').any()
    print(f"{col}: special chars remain = {has_bad}")