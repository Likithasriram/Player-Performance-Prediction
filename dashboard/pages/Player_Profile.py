## dashboard/pages/Player_Profile.py
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import os
import io
import plotly.express as px
import importlib

# --- robust import for predict_module ---
# Attempts to import predict_batsman/predict_bowler from multiple locations:
#  - top-level predict_module (project root)
#  - Scripts.predict_module (Scripts folder)
# If import fails, falls back to safe placeholder functions.
_predict_batsman = None
_predict_bowler = None

for module_name in ("predict_module", "Scripts.predict_module"):
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, "predict_batsman") and hasattr(mod, "predict_bowler"):
            _predict_batsman = getattr(mod, "predict_batsman")
            _predict_bowler = getattr(mod, "predict_bowler")
            break
    except Exception:
        continue

if _predict_batsman is None or _predict_bowler is None:
    # fallback placeholder functions (safe, simple heuristics)
    def _predict_batsman(balls_faced: float, strike_rate: float, dot_ball_pct: float) -> float:
        try:
            bf = float(balls_faced)
            sr = float(strike_rate)
            dot = float(dot_ball_pct)
        except Exception:
            raise ValueError("Invalid numeric inputs for predict_batsman")
        small_adjust = 0.95
        pred = bf * (sr / 100.0) * (1.0 - dot / 100.0) * small_adjust
        return float(max(0.0, pred))

    def _predict_bowler(overs: float, economy: float, dot_ball_pct: float) -> float:
        try:
            o = float(overs)
            eco = float(economy)
            dot = float(dot_ball_pct)
        except Exception:
            raise ValueError("Invalid numeric inputs for predict_bowler")
        base = o * (dot / 100.0) * 0.6
        penalty = max(0.0, (eco - 6.0) * 0.05)
        pred = max(0.0, base - penalty)
        return float(pred)

# expose names used later in the file
predict_batsman = _predict_batsman
predict_bowler = _predict_bowler
# --- end import section ---

# ---------------------- paths ----------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data_clean"
OUTPUTS_DIR = BASE_DIR / "outputs"

# ---------------------- small helpers ----------------------
def safe_read(path):
    if not path:
        return pd.DataFrame()
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except Exception:
        return pd.DataFrame()

def detect_player_col(df):
    """Return column name likely containing player identity (lowercase)."""
    if df is None or df.empty:
        return None
    cols = [c.lower().strip() for c in df.columns]
    for name in ["player", "batsman", "bowler", "name"]:
        if name in cols:
            return cols[cols.index(name)]
    # fallback heur: try any object dtype column
    for orig_c in df.columns:
        c = orig_c.lower().strip()
        if df[orig_c].dtype == object:
            return c
    return None

def detect_forecast_value_col(df, desired=None):
    if desired is None:
        desired = ["forecasted_runs", "forecasted_wickets", "forecast", "pred", "value", "y_pred"]
    if df is None or df.empty:
        return None
    cols = [c.lower().strip() for c in df.columns]
    for name in desired:
        if name in cols:
            return cols[cols.index(name)]
    # fallback numeric column other than matchId/season etc.
    numeric_cols = []
    for orig_c in df.columns:
        c = orig_c.lower().strip()
        try:
            if pd.api.types.is_numeric_dtype(df[orig_c]) and "id" not in c:
                numeric_cols.append(c)
        except Exception:
            continue
    return numeric_cols[0] if numeric_cols else None

# ---------------------- load forecast CSVs (cached) ----------------------
@st.cache_data(ttl=300)
def load_forecasts():
    files = {}
    # common names used in this repo
    candidates = {
        "batsman": OUTPUTS_DIR / "batsman_forecast_form.csv",
        "bowler": OUTPUTS_DIR / "bowler_forecast_form.csv",
        "next_5": OUTPUTS_DIR / "next_5_matches_forecast.csv",
    }
    for k, p in candidates.items():
        files[k] = safe_read(p)
    # also attempt to pick any CSVs in outputs/ that contain 'forecast' in name
    try:
        for p in OUTPUTS_DIR.glob("*.csv"):
            key = p.name.lower()
            if "forecast" in key and p.name not in [c.name for c in candidates.values()]:
                files[p.name] = safe_read(p)
    except Exception:
        pass
    return files

forecast_files = load_forecasts()

# ---------------------- robust load_main ----------------------
@st.cache_data(ttl=300)
def load_main():
    """
    Try common filenames in DATA_DIR and return (bats_df, bowl_df, bats_path, bowl_path).
    """
    bats_candidates = [
        "clean_batsman.csv", "clean_batsmen.csv",
        "batsman_feat_eng.csv", "batsman.csv", "batsmen.csv"
    ]
    bowl_candidates = [
        "clean_bowler.csv", "bowler_feat_eng.csv", "bowler.csv"
    ]

    def find_and_read(candidates):
        for fn in candidates:
            p = DATA_DIR / fn
            if p.exists():
                try:
                    df = pd.read_csv(p)
                    # normalize columns: lowercase + strip
                    df.columns = [c.strip() for c in df.columns]
                    # keep a lowercase-mapped copy for detection but do not change original names here
                    return df, str(p)
                except Exception:
                    continue
        return pd.DataFrame(), None

    bats_df, bats_path = find_and_read(bats_candidates)
    bowl_df, bowl_path = find_and_read(bowl_candidates)

    # normalize column names to lowercase for consistent downstream usage
    if not bats_df.empty:
        bats_df.columns = [c.lower().strip() for c in bats_df.columns]
    if not bowl_df.empty:
        bowl_df.columns = [c.lower().strip() for c in bowl_df.columns]

    return bats_df, bowl_df, bats_path, bowl_path

batsman_df, bowler_df, bats_path, bowl_path = load_main()

# show debug info in sidebar
#st.sidebar.markdown("**Data files (debug)**")
#st.sidebar.write(f"data_clean exists: {DATA_DIR.exists()}")
#st.sidebar.write(f"Batsman file: {bats_path or 'none'}")
#st.sidebar.write(f"Bowler file: {bowl_path or 'none'}")

# ---------------------- UI styling ----------------------
st.markdown("""
<style>
.card { background: rgba(255,255,255,0.03); padding: 18px; border-radius: 12px; border:1px solid rgba(255,255,255,0.06); margin-bottom:12px; }
.kpi-title { color:#9aa7b8; font-size:0.9rem; }
.kpi-value { font-size:1.5rem; font-weight:700; margin-top:6px; }
.small-muted { color:#97a0ab; font-size:0.85rem; }
.section-title { font-size:1.2rem; font-weight:600; margin-bottom:8px; }
</style>
""", unsafe_allow_html=True)

# ---------------------- sidebar player list (robust) ----------------------
st.sidebar.header("🔎 Choose player")
role = st.sidebar.radio("Role", ["Batsman", "Bowler"])

# detect player column name inside each loaded df (lowercase)
bats_player_col = detect_player_col(batsman_df) if not batsman_df.empty else None
bowl_player_col = detect_player_col(bowler_df) if not bowler_df.empty else None

if role == "Batsman":
    if batsman_df.empty or bats_player_col is None:
        players = []
    else:
        players = sorted(batsman_df[bats_player_col].dropna().astype(str).unique().tolist())
else:
    if bowler_df.empty or bowl_player_col is None:
        players = []
    else:
        players = sorted(bowler_df[bowl_player_col].dropna().astype(str).unique().tolist())

if not players:
    st.sidebar.warning("No players found in data_clean/. Check CSV names and player column names. (See debug above).")
    st.stop()

player = st.sidebar.selectbox("Player", ["-- choose --"] + players)
if player == "-- choose --":
    st.sidebar.info("Pick a player to see profile")
    st.stop()

# ---------------------- filter historical rows ----------------------
if role == "Batsman":
    if bats_player_col and bats_player_col in batsman_df.columns:
        rows = batsman_df[batsman_df[bats_player_col].astype(str) == str(player)].copy()
    else:
        rows = pd.DataFrame()
else:
    if bowl_player_col and bowl_player_col in bowler_df.columns:
        rows = bowler_df[bowler_df[bowl_player_col].astype(str) == str(player)].copy()
    else:
        rows = pd.DataFrame()

# ---------------------- header & KPIs ----------------------
st.title(player)
st.caption(f"Role: {role}")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if role == "Batsman":
        val = rows["effective_runs"].mean() if "effective_runs" in rows.columns and not rows.empty else np.nan
        st.markdown("<div class='card'><div class='kpi-title'>Avg Effective Runs</div><div class='kpi-value'>{:.2f}</div></div>".format(val if not np.isnan(val) else 0), unsafe_allow_html=True)
    else:
        val = rows["effective_wickets"].mean() if "effective_wickets" in rows.columns and not rows.empty else np.nan
        st.markdown("<div class='card'><div class='kpi-title'>Avg Effective Wickets</div><div class='kpi-value'>{:.2f}</div></div>".format(val if not np.isnan(val) else 0), unsafe_allow_html=True)

with col2:
    if role == "Batsman":
        val = rows["balls_faced"].mean() if "balls_faced" in rows.columns and not rows.empty else np.nan
        st.markdown("<div class='card'><div class='kpi-title'>Avg Balls Faced</div><div class='kpi-value'>{:.1f}</div></div>".format(val if not np.isnan(val) else 0), unsafe_allow_html=True)
    else:
        val = rows["economy"].mean() if "economy" in rows.columns and not rows.empty else np.nan
        st.markdown("<div class='card'><div class='kpi-title'>Avg Economy</div><div class='kpi-value'>{:.2f}</div></div>".format(val if not np.isnan(val) else 0), unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='card'><div class='kpi-title'>Records Available</div><div class='kpi-value'>{len(rows)}</div></div>", unsafe_allow_html=True)

st.write("---")

# ---------------------- layout: left predict, right history+forecast ----------------------
left, right = st.columns([1.2, 2], gap="large")

# left: predict
with left:
    st.subheader("🎯 Quick predict")
    recent = rows.head(5)
    # defaults
    def safe_mean(col, default=0.0):
        try:
            return float(recent[col].mean()) if col in recent.columns and not recent.empty else float(default)
        except Exception:
            return float(default)

    if role == "Batsman":
        balls = st.number_input("Balls faced", value=safe_mean("balls_faced", 30.0))
        sr = st.number_input("Strike rate", value=safe_mean("strike_rate", 120.0))
        dot = st.number_input("Dot ball %", value=safe_mean("dot_ball_pct", 25.0))
        if st.button("Predict runs"):
            try:
                pred = predict_batsman(balls, sr, dot)
                st.success(f"🏏 Predicted Effective Runs: {pred:.2f}")
            except Exception as e:
                st.error(f"Prediction error: {e}")
    else:
        overs = st.number_input("Overs", value=safe_mean("overs", 4.0))
        eco = st.number_input("Economy", value=safe_mean("economy", 7.5))
        dot = st.number_input("Dot ball %", value=safe_mean("dot_ball_pct", 30.0))
        if st.button("Predict wickets"):
            try:
                pred = predict_bowler(overs, eco, dot)
                st.success(f"🎯 Predicted Effective Wickets: {pred:.2f}")
            except Exception as e:
                st.error(f"Prediction error: {e}")

# right: recent + forecast
with right:
    st.subheader("📘 Recent matches")
    if rows.empty:
        st.info("No historical rows available.")
    else:
        # columns we prefer to show (lowercase)
        preferred = [
            'matchid','season','venue','batting_team','bowling_team',
            'balls_faced','strike_rate','effective_runs',
            'overs','economy','effective_wickets','dot_ball_pct'
        ]
        display_cols = [c for c in preferred if c in rows.columns]
        if display_cols:
            st.dataframe(rows.reset_index(drop=True)[display_cols].head(50), use_container_width=True, height=320)
        else:
            st.dataframe(rows.reset_index(drop=True).head(50), use_container_width=True, height=320)

    st.write("")  # spacing

    # ---------------------- LSTM Forecast block ----------------------
    st.subheader("📈 LSTM Forecast (next matches)")
    # pick forecast df depending on role
    forecast_df = None
    if role == "Batsman" and "batsman" in forecast_files and not forecast_files["batsman"].empty:
        forecast_df = forecast_files["batsman"]
    elif role == "Bowler" and "bowler" in forecast_files and not forecast_files["bowler"].empty:
        forecast_df = forecast_files["bowler"]
    elif "next_5" in forecast_files and not forecast_files["next_5"].empty:
        forecast_df = forecast_files["next_5"]
    else:
        # try any other forecast-like file
        for k, df in forecast_files.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                forecast_df = df
                break

    if forecast_df is None or forecast_df.empty:
        st.info("No forecast CSV found in outputs/ or file is empty. Expected names: batsman_forecast_form.csv, bowler_forecast_form.csv or next_5_matches_forecast.csv")
    else:
        # normalize forecast_df columns to lowercase for detection
        forecast_df.columns = [c.lower().strip() for c in forecast_df.columns]
        player_col = detect_player_col(forecast_df)
        value_col = detect_forecast_value_col(forecast_df)

        if player_col is None or value_col is None:
            st.warning("Forecast file loaded but I couldn't detect player/value columns automatically. Please inspect your outputs CSV.")
            st.dataframe(forecast_df.head())
        else:
            # filter for this player (case-insensitive match)
            fdf = forecast_df[forecast_df[player_col].astype(str).str.lower() == str(player).lower()].copy()
            if fdf.empty:
                st.info("No forecast rows found for this player in the forecast CSV.")
                # show small sample for debugging
                st.expander("See sample of loaded forecast file").dataframe(forecast_df.head(10))
            else:
                # create index for match number if not present
                idx_col = None
                for c in ["match_no", "match_index", "game", "fixture", "match_number", "seq"]:
                    if c in fdf.columns:
                        idx_col = c
                        break
                if idx_col is None:
                    fdf = fdf.reset_index(drop=True)
                    fdf["seq"] = fdf.index + 1
                    x_col = "seq"
                else:
                    x_col = idx_col

                # sort by x_col if numeric
                try:
                    fdf = fdf.sort_values(by=x_col)
                except Exception:
                    pass

                # ensure value column numeric
                fdf[value_col] = pd.to_numeric(fdf[value_col], errors="coerce")

                # build plotly chart
                title = f"Forecast for {player} — {value_col}"
                fig = px.line(fdf, x=x_col, y=value_col, markers=True, title=title)
                fig.update_layout(template="plotly_dark", height=360, margin=dict(t=40, b=20, l=30, r=10))
                st.plotly_chart(fig, use_container_width=True)

                # download filtered forecast for this player
                csv_bytes = fdf.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download player forecast CSV",
                    data=csv_bytes,
                    file_name=f"{player}_forecast.csv",
                    mime="text/csv",
                )

st.write("---")
st.caption("Forecasts loaded from outputs/. If your forecast filenames differ, place them in outputs/ and follow naming patterns (batsman_forecast_form.csv / bowler_forecast_form.csv / next_5_matches_forecast.csv).")
