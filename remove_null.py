import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/employer_branding_original.xlsx")

PROCESSED_PATH = Path("data/processed/employer_branding_clean.xlsx")

def save_processed(df):
    df.to_excel(PROCESSED_PATH, index=False)
    print(f"\nProcessed data saved to: {PROCESSED_PATH}")

def load_data():
    return pd.read_excel(RAW_PATH)

def fill_missing_with_mean(df):
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    return df

if __name__ == "__main__":
    df = load_data()
    print("\n--- IMPUTING MISSING VALUES WITH MEAN ---")

    df = fill_missing_with_mean(df)

    print("\n--- MISSING VALUES AFTER IMPUTATION ---")
    print(df.isna().sum())

    save_processed(df)

