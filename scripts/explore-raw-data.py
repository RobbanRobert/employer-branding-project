import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/employer_branding_original.xlsx")

def load_data():
    return pd.read_excel(RAW_PATH)

def explore(df):
    print("\n--- SHAPE ---")
    print(df.shape)

    print("\n--- COLUMNS ---")
    print(df.columns.tolist())

    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

    print("\n--- SAMPLE ROWS ---")
    print(df.head())

if __name__ == "__main__":
    df = load_data()
    explore(df)