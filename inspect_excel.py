
import pandas as pd

try:
    df = pd.read_excel("linelist_cleaned.xlsx")
    print("Columns found:", df.columns.tolist())
    print("First few rows:\n", df.head())
except Exception as e:
    print(f"Error reading file: {e}")
