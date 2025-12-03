import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

# File paths
CLEAN_BOWLER = "data_clean/clean_bowler.csv"
CLEAN_BATSMAN = "data_clean/clean_batsmen.csv"

BOWLER_MODEL_PATH = "models/bowler_model.pkl"
BATSMAN_MODEL_PATH = "models/batsman_model.pkl"

BOWLER_SCALER_PATH = "models/bowler_scaler.pkl"
BATSMAN_SCALER_PATH = "models/batsman_scaler.pkl"


# --------------------------
#  TRAIN BOWLER MODEL
# --------------------------
def train_bowler():
    print("\n🔹 Training Bowler Model...")

    df = pd.read_csv(CLEAN_BOWLER)

    features = ['overs', 'economy', 'dot_ball_pct']
    target = 'effective_wickets'

    df = df.dropna(subset=features + [target])

    X = df[features]
    y = df[target]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    joblib.dump(scaler, BOWLER_SCALER_PATH)
    print("💾 Bowler scaler saved.")

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, BOWLER_MODEL_PATH)
    print("💾 Bowler model saved.")

    print("✅ Bowler model training complete!")


# --------------------------
#  TRAIN BATSMAN MODEL
# --------------------------
def train_batsman():
    print("\n🔹 Training Batsman Model...")

    df = pd.read_csv(CLEAN_BATSMAN)

    features = ['balls_faced', 'strike_rate', 'dot_ball_pct']
    target = 'effective_runs'

    df = df.dropna(subset=features + [target])

    X = df[features]
    y = df[target]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    joblib.dump(scaler, BATSMAN_SCALER_PATH)
    print("💾 Batsman scaler saved.")

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, BATSMAN_MODEL_PATH)
    print("💾 Batsman model saved.")

    print("✅ Batsman model training complete!")


# --------------------------
#  MAIN
# --------------------------
if __name__ == "__main__":
    train_bowler()
    train_batsman()
    print("\n🎉 All models trained successfully!")
