import pandas as pd
import os

# Paths
RAW_BATSMAN_PATH = r"C:\Users\91939\OneDrive\Desktop\player performance prediction\data_raw\batsman_feat_eng.csv"
RAW_BOWLER_PATH = r"C:\Users\91939\OneDrive\Desktop\player performance prediction\data_raw\bowler_feat_eng.csv"

CLEAN_BATSMAN_PATH = "data_clean/clean_batsmen.csv"
CLEAN_BOWLER_PATH = "data_clean/clean_bowler.csv"


def clean_file(input_path, output_path):
    print(f"🔄 Reading dataset → {input_path}")
    df = pd.read_csv(input_path)

    print("🔄 Dropping duplicates...")
    df.drop_duplicates(inplace=True)

    print("🔄 Handling missing values...")
    df.fillna(method='bfill', inplace=True)
    df.fillna(method='ffill', inplace=True)

    print("🔄 Converting datatypes when possible...")
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    print("💾 Saving cleaned dataset...")
    os.makedirs("data_clean", exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"✔ Saved clean file → {output_path}\n")


def run_etl():
    print("🚀 Starting ETL Pipeline...\n")

    clean_file(RAW_BATSMAN_PATH, CLEAN_BATSMAN_PATH)
    clean_file(RAW_BOWLER_PATH, CLEAN_BOWLER_PATH)

    print("🎯 ETL Completed Successfully!")


if __name__ == "__main__":
    run_etl()
