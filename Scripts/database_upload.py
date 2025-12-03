# database_upload.py
# Scripts/database_upload.py
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from math import ceil

# ------------------------------
# DATABASE CONFIG (use env vars when possible)
# ------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "liki@1220")  # consider using env var instead of hard-coding
DB_NAME = os.getenv("DB_NAME", "player_prediction_db")

# CSV paths (match filenames you used in training)
BOWLER_CSV = os.path.join("data_clean", "clean_bowler.csv")
BATSMAN_CSV = os.path.join("data_clean", "clean_batsmen.csv")  # note: singular 'batsman' to match model_training.py

# Insert chunk size
CHUNK_SIZE = 1000


# ------------------------------
# DB helpers
# ------------------------------
def get_connection(database=None):
    kwargs = dict(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    if database:
        kwargs["database"] = database
    return mysql.connector.connect(**kwargs)


def create_database():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"📁 Database '{DB_NAME}' is ready.")
    except Error as e:
        print("❌ Error creating database:", e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ------------------------------
# Table creation
# ------------------------------
def create_bowler_table():
    conn = None
    cursor = None
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS bowler_performance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            overs FLOAT,
            economy FLOAT,
            dot_ball_pct FLOAT,
            effective_wickets FLOAT
        ) ENGINE=InnoDB;
        """
        cursor.execute(query)
        conn.commit()
        print("📄 Table 'bowler_performance' is ready.")
    except Error as e:
        print("❌ Error creating bowler table:", e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_batsman_table():
    conn = None
    cursor = None
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS batsman_performance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            matchId INT,
            season VARCHAR(50),
            venue VARCHAR(255),
            batting_team VARCHAR(255),
            bowling_team VARCHAR(255),
            batsman VARCHAR(255),
            total_runs_off_bat INT,
            is_boundary INT,
            is_dotball INT,
            balls_faced INT,
            strike_rate FLOAT,
            dot_ball_pct FLOAT,
            effective_runs FLOAT,
            winner VARCHAR(255),
            player_of_match VARCHAR(255),
            toss_winner VARCHAR(255),
            toss_decision VARCHAR(50)
        ) ENGINE=InnoDB;
        """
        cursor.execute(query)
        conn.commit()
        print("📄 Table 'batsman_performance' is ready.")
    except Error as e:
        print("❌ Error creating batsman table:", e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ------------------------------
# Data upload helpers
# ------------------------------
def read_csv_checked(path, required_columns=None):
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    df = pd.read_csv(path)
    if required_columns:
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns in {path}: {missing}")
        # Keep only required cols in defined order
        df = df[required_columns]
    return df


def insert_in_chunks(conn, cursor, insert_query, data_list, chunk_size=CHUNK_SIZE):
    total = len(data_list)
    if total == 0:
        return 0
    chunks = ceil(total / chunk_size)
    inserted = 0
    for i in range(chunks):
        chunk = data_list[i * chunk_size: (i + 1) * chunk_size]
        cursor.executemany(insert_query, chunk)
        conn.commit()
        inserted += cursor.rowcount
    return inserted


# ------------------------------
# Upload functions
# ------------------------------
def upload_bowler_data(truncate=False):
    required_cols = ['overs', 'economy', 'dot_ball_pct', 'effective_wickets']
    df = read_csv_checked(BOWLER_CSV, required_columns=required_cols)

    # Drop rows with missing critical values
    df = df.dropna(subset=required_cols)

    conn = None
    cursor = None
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        if truncate:
            cursor.execute("TRUNCATE TABLE bowler_performance")
            conn.commit()

        query = """
        INSERT INTO bowler_performance (overs, economy, dot_ball_pct, effective_wickets)
        VALUES (%s, %s, %s, %s)
        """
        # convert NaN -> None and ensure object dtype so None is preserved
        data = df[required_cols].astype(object).where(pd.notnull(df), None).values.tolist()
        inserted = insert_in_chunks(conn, cursor, query, data)
        print(f"✅ {inserted} bowler rows inserted successfully!")
    except Error as e:
        print("❌ Error uploading bowler data:", e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def upload_batsman_data(truncate=False):
    required_cols = [
        'matchId','season','venue','batting_team','bowling_team','batsman',
        'total_runs_off_bat','is_boundary','is_dotball','balls_faced',
        'strike_rate','dot_ball_pct','effective_runs',
        'winner','player_of_match','toss_winner','toss_decision'
    ]
    df = read_csv_checked(BATSMAN_CSV, required_columns=required_cols)

    # Convert NaN -> None safely and preserve object dtype so None is preserved in lists
    df = df.astype(object).where(pd.notnull(df), None)

    conn = None
    cursor = None
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        if truncate:
            cursor.execute("TRUNCATE TABLE batsman_performance")
            conn.commit()

        query = """
        INSERT INTO batsman_performance (
            matchId, season, venue, batting_team, bowling_team, batsman,
            total_runs_off_bat, is_boundary, is_dotball, balls_faced,
            strike_rate, dot_ball_pct, effective_runs,
            winner, player_of_match, toss_winner, toss_decision
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = df[required_cols].values.tolist()
        inserted = insert_in_chunks(conn, cursor, query, data)
        print(f"✅ {inserted} batsman rows inserted successfully!")
    except Error as e:
        print("❌ Error uploading batsman data:", e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    # Create DB/tables if needed
    create_database()
    create_bowler_table()
    create_batsman_table()

    # Upload data (set truncate=True if you want to replace existing data)
    upload_bowler_data(truncate=False)
    upload_batsman_data(truncate=False)

    print("🎉 All data uploaded successfully!")
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=["all","bowler","batsman"], default="all",
                        help="Choose which dataset to upload")
    parser.add_argument("--truncate", action="store_true", help="Truncate table(s) before uploading")
    args = parser.parse_args()

    create_database()
    create_bowler_table()
    create_batsman_table()

    if args.only in ("all","bowler"):
        upload_bowler_data(truncate=args.truncate)
    if args.only in ("all","batsman"):
        upload_batsman_data(truncate=args.truncate)

    print("🎉 Done.")
