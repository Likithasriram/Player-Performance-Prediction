# Scripts/create_samples.py
import os
import pandas as pd
import mysql.connector
import shutil

os.makedirs("data_sample", exist_ok=True)

print("Connecting to MySQL...")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="liki@1220",
    database="player_prediction_db"
)

print("Exporting batsman_sample.csv (200 rows)...")
pd.read_sql("SELECT * FROM batsman_performance LIMIT 200", conn).to_csv("data_sample/batsman_sample.csv", index=False)

print("Exporting bowler_sample.csv (200 rows)...")
pd.read_sql("SELECT * FROM bowler_performance LIMIT 200", conn).to_csv("data_sample/bowler_sample.csv", index=False)

# optional: copy forecast if it exists
if os.path.exists("outputs/next_5_matches_forecast.csv"):
    print("Copying forecast sample...")
    shutil.copy("outputs/next_5_matches_forecast.csv", "data_sample/next_5_matches_forecast_sample.csv")

conn.close()
print("data_sample CSVs created in ./data_sample/")
