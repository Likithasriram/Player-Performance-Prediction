# dashboard/db_utils.py
import os
from dotenv import load_dotenv
import pandas as pd
import mysql.connector
from streamlit import cache_data

load_dotenv()  # load .env

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data_sample")

def _mysql_connect():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, connection_timeout=10
    )

@cache_data(ttl=600)
def load_batsman(limit=5000):
    if DB_HOST and DB_USER and DB_PASSWORD and DB_NAME:
        try:
            conn = _mysql_connect()
            df = pd.read_sql(f"SELECT * FROM batsman_performance LIMIT {limit}", conn)
            conn.close()
            return df
        except Exception:
            pass
    sample_path = os.path.join(SAMPLE_DIR, "batsman_sample.csv")
    return pd.read_csv(sample_path)

@cache_data(ttl=600)
def load_bowler(limit=5000):
    if DB_HOST and DB_USER and DB_PASSWORD and DB_NAME:
        try:
            conn = _mysql_connect()
            df = pd.read_sql(f"SELECT * FROM bowler_performance LIMIT {limit}", conn)
            conn.close()
            return df
        except Exception:
            pass
    sample_path = os.path.join(SAMPLE_DIR, "bowler_sample.csv")
    return pd.read_csv(sample_path)

@cache_data(ttl=600)
def load_forecast():
    repo_forecast = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs", "next_5_matches_forecast.csv")
    if os.path.exists(repo_forecast):
        return pd.read_csv(repo_forecast)
    sample_forecast = os.path.join(SAMPLE_DIR, "next_5_matches_forecast_sample.csv")
    if os.path.exists(sample_forecast):
        return pd.read_csv(sample_forecast)
    return pd.DataFrame()
