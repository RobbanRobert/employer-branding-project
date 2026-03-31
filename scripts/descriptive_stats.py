import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path("Working file Employer Branding.xlsx")

df = pd.read_excel(RAW_PATH)

# ── Column groups ──────────────────────────────────────────────────────────────
emapat_cols = [c for c in df.columns if c.startswith("EmpAt")]
cr_cols     = [c for c in df.columns if c.startswith("CR")]
ia_cols     = [c for c in df.columns if c.startswith("IA")]
coo_cols    = [c for c in df.columns if c.startswith("CoO")]
likert_cols = emapat_cols + cr_cols + ia_cols + coo_cols

demo_cols   = ["Gender", "Age_NEW", "Education_NEW", "Work_experience"]

# ── Recode out-of-range values (9 on 1–7 scale → NaN) ────────────────────────
for col in emapat_cols + cr_cols + ia_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[df[col] == 9, col] = np.nan

# ── 1. Likert scale descriptives ──────────────────────────────────────────────
print("=" * 60)
print("LIKERT SCALE DESCRIPTIVES (1–7)")
print("=" * 60)

scale_groups = {
    "Employer Attractiveness (EmpAt)": emapat_cols,
    "Corporate Reputation (CR)":       cr_cols,
    "Intention to Apply (IA)":         ia_cols,
    "Country of Origin (CoO)":         coo_cols,
}

for group_name, cols in scale_groups.items():
    print(f"\n--- {group_name} ---")
    stats = df[cols].agg(["mean", "std", "min", "max", "count"]).T
    stats["missing"] = df[cols].isna().sum().values
    stats.columns = ["Mean", "SD", "Min", "Max", "N", "Missing"]
    stats = stats.round(2)
    print(stats.to_string())

# ── 2. Composite scale scores ─────────────────────────────────────────────────
print("\n" + "=" * 60)
print("COMPOSITE SCALE SCORES (mean of items)")
print("=" * 60)

subscales = {
    "EmpAt_Interest":    ["EmpAt_10", "EmpAt_11", "EmpAt_12", "EmpAt_13", "EmpAt_14"],
    "EmpAt_Social":      ["EmpAt_2",  "EmpAt_7",  "EmpAt_8",  "EmpAt_9",  "EmpAt_23"],
    "EmpAt_Economic":    ["EmpAt_15", "EmpAt_21", "EmpAt_22", "EmpAt_24", "EmpAt_25"],
    "EmpAt_Development": ["EmpAt_1",  "EmpAt_3",  "EmpAt_4",  "EmpAt_5",  "EmpAt_6"],
    "EmpAt_Application": ["EmpAt_16", "EmpAt_17", "EmpAt_18", "EmpAt_19", "EmpAt_20"],
    "EmpAt_Total":       emapat_cols,
    "CR_Mean":           cr_cols,
    "IA_Mean":           ia_cols,
    "CoO_Mean":          coo_cols,
}

for name, items in subscales.items():
    df[name] = df[items].mean(axis=1)

composite_cols = list(subscales.keys())
stats = df[composite_cols].agg(["mean", "std", "min", "max"]).T.round(2)
stats.columns = ["Mean", "SD", "Min", "Max"]
print(stats.to_string())

# ── 3. Demographic distributions ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("DEMOGRAPHIC DISTRIBUTIONS")
print("=" * 60)

gender_map   = {1: "Male", 2: "Female"}
age_map      = {1: "Group 1", 2: "Group 2", 3: "Group 3", 4: "Group 4"}
edu_map      = {1: "Engineering/Technical", 2: "Business/Economics",
                3: "Law/Social science",   4: "Other"}
workexp_map  = {1: "No experience", 2: "Up to 1 year",
                3: "1–2 years",     4: "More than 2 years"}

demo_info = {
    "Gender":         (gender_map,  df["Gender"].replace(3, np.nan)),
    "Age group":      (age_map,     df["Age_NEW"]),
    "Education":      (edu_map,     df["Education_NEW"]),
    "Work experience":(workexp_map, df["Work_experience"]),
}

for label, (mapping, series) in demo_info.items():
    print(f"\n--- {label} ---")
    counts = series.value_counts().sort_index()
    pct    = (counts / counts.sum() * 100).round(1)
    table  = pd.DataFrame({"N": counts, "%": pct})
    table.index = table.index.map(lambda x: mapping.get(x, x))
    print(table.to_string())