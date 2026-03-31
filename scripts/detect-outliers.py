import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/employer_branding_original.xlsx")

def load_data():
    return pd.read_excel(RAW_PATH)

def detect_outliers_iqr(df, cols):
    outliers = {}
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers[col] = df[(df[col] < lower) | (df[col] > upper)][col]
    return outliers

def get_numeric_columns(df):
    return df.select_dtypes(include=['int64', 'float64']).columns

if __name__ == "__main__":
    df = load_data()
    cols = get_numeric_columns(df)
    outliers = detect_outliers_iqr(df, cols)

    print("\n--- OUTLIERS FOUND ---")
    for col, values in outliers.items():
        if len(values) > 0:
            print(f"\n{col}:")
            print(values)
