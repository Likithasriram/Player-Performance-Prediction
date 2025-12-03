import argparse
import os
import sys
import pandas as pd
from joblib import load
import numpy as np

# -----------------------------
# Resolve project BASE_DIR
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to models and scalers
BATSMAN_MODEL_PATH = os.path.join(BASE_DIR, "models", "batsman_model.pkl")
BATSMAN_SCALER_PATH = os.path.join(BASE_DIR, "models", "batsman_scaler.pkl")

BOWLER_MODEL_PATH = os.path.join(BASE_DIR, "models", "bowler_model.pkl")
BOWLER_SCALER_PATH = os.path.join(BASE_DIR, "models", "bowler_scaler.pkl")


# -----------------------------
# Utility loaders
# -----------------------------
def safe_load(path, name="object"):
    if not os.path.exists(path):
        print(f"❌ ERROR: {name} not found at: {path}")
        sys.exit(1)
    try:
        return load(path)
    except Exception as e:
        print(f"❌ ERROR loading {name} at: {path}\n   → {e}")
        sys.exit(1)


# -----------------------------
# Prediction functions
# -----------------------------
def predict_batsman(args):
    print(f"📌 Loading batsman model from: {BATSMAN_MODEL_PATH}")

    model = safe_load(BATSMAN_MODEL_PATH, "Batsman model")
    scaler = safe_load(BATSMAN_SCALER_PATH, "Batsman scaler")

    # Feature names must match what scaler/model were trained with
    feature_df = pd.DataFrame(
        [[args.balls_faced, args.strike_rate, args.dot_ball_pct]],
        columns=["balls_faced", "strike_rate", "dot_ball_pct"]
    )

    features_scaled = scaler.transform(feature_df)
    pred = model.predict(features_scaled)[0]

    print(f"\n🏏 Predicted Effective Runs (batsman): {pred:.2f}")


def predict_bowler(args):
    print(f"📌 Loading bowler model from: {BOWLER_MODEL_PATH}")

    model = safe_load(BOWLER_MODEL_PATH, "Bowler model")
    scaler = safe_load(BOWLER_SCALER_PATH, "Bowler scaler")

    feature_df = pd.DataFrame(
        [[args.overs, args.economy, args.dot_ball_pct]],
        columns=["overs", "economy", "dot_ball_pct"]
    )

    features_scaled = scaler.transform(feature_df)
    pred = model.predict(features_scaled)[0]

    print(f"\n🎯 Predicted Effective Wickets (bowler): {pred:.2f}")


# -----------------------------
# CLI parsing
# -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Predict batsman or bowler performance.")

    parser.add_argument("--type", required=True, choices=["batsman", "bowler"],
                        help="Select prediction type")

    # Batsman features
    parser.add_argument("--balls_faced", type=float)
    parser.add_argument("--strike_rate", type=float)

    # Common feature
    parser.add_argument("--dot_ball_pct", type=float, required=True)

    # Bowler features
    parser.add_argument("--overs", type=float)
    parser.add_argument("--economy", type=float)

    args = parser.parse_args()

    # Validation
    if args.type == "batsman":
        if args.balls_faced is None or args.strike_rate is None:
            parser.error("Batsman requires: --balls_faced --strike_rate --dot_ball_pct")
    else:
        if args.overs is None or args.economy is None:
            parser.error("Bowler requires: --overs --economy --dot_ball_pct")

    return args


# -----------------------------
# MAIN
# -----------------------------
def main():
    args = parse_args()

    if args.type == "batsman":
        predict_batsman(args)
    else:
        predict_bowler(args)


if __name__ == "__main__":
    main()
