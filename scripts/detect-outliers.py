import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/employer_branding_original.xlsx")

def load_data():
    return pd.read_excel(RAW_PATH)

def get_numeric_columns(df):
    return df.select_dtypes(include=['int64', 'float64']).columns

def get_likert_columns(df):
    prefixes = ("EmpAt_", "CR_", "IA_", "CoO_")
    return [col for col in df.columns if col.startswith(prefixes)]

def get_numeric_non_likert(df):
    numeric = get_numeric_columns(df)
    likert = get_likert_columns(df)
    return [col for col in numeric if col not in likert]

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

# gränserna för likert är 1-7
def check_likert_ranges(df, min_val=1, max_val=7):
    likert_cols = get_likert_columns(df)
    errors = {}
    for col in likert_cols:
        bad_values = df[(df[col] < min_val) | (df[col] > max_val)][col]
        if len(bad_values) > 0:
            errors[col] = bad_values
    return errors

if __name__ == "__main__":
    df = load_data()
    cols = get_numeric_non_likert(df)
    outliers = detect_outliers_iqr(df, cols)

    likert_errors = check_likert_ranges(df)

    print("\n--- LIKERT RANGE ERRORS ---")
    for col, values in likert_errors.items():
        print(f"\n{col}:")
        print(values)

    print("\n--- OUTLIERS FOUND ---")
    for col, values in outliers.items():
        if len(values) > 0:
            print(f"\n{col}:")
            print(values)
