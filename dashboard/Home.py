# dashboard/Home.py
import streamlit as st
import os
from pathlib import Path
import pandas as pd

BASE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUTS = BASE / "outputs"

st.set_page_config(page_title="Player Performance Predictor", layout="wide")
st.markdown("""
<style>
/* subtle dark card look */
.card { padding: 18px; border-radius: 10px; background-color: rgba(255,255,255,0.02); }
.center { text-align:center }
.small-muted { color: #bfc9d1; font-size:0.95rem }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='center'><h1>🏏 Player Performance Predictor</h1></div>", unsafe_allow_html=True)
st.markdown("<p class='center small-muted'>Player-focused ML & time-series forecasting — pick a player to see history, model prediction & forecast.</p>", unsafe_allow_html=True)
st.write("---")

# Top metrics row (compact)
col1, col2, col3 = st.columns([1,1,1])
def safe_count(path):
    if path.exists():
        try:
            return len(pd.read_csv(path))
        except Exception:
            return "–"
    return "–"

col1.metric("Batsman forecasts", safe_count(OUTPUTS / "batsman_forecast_form.csv"))
col2.metric("Bowler forecasts", safe_count(OUTPUTS / "bowler_forecast_form.csv"))
col3.metric("Combined forecasts", safe_count(OUTPUTS / "next_5_matches_forecast.csv"))

st.write("")
left, right = st.columns([1.6, 1])

# --------- helper: set query param safely and rerun safely ----------
def set_page_query_param(key: str, value: str):
    """
    Try to set query params using available Streamlit API.
    Newer API: st.query_params (assignable dict-like)
    Some older versions: st.set_query_params(...)
    Fallback: set a value in session_state so app can read it.
    """
    try:
        # preferred: assign to st.query_params (works on newer versions)
        st.query_params[key] = value
        return
    except Exception:
        pass

    try:
        # alternative API if available
        set_q = getattr(st, "set_query_params", None)
        if callable(set_q):
            set_q(**{key: value})
            return
    except Exception:
        pass

    # final fallback
    st.session_state[f"query_{key}"] = value


def safe_rerun():
    """
    Attempt to rerun the app using st.rerun(), otherwise no-op.
    """
    try:
        st.rerun()
    except Exception:
        # if rerun is unavailable just continue (no crash)
        return

# ---------------------------- UI ----------------------------
with left:
    st.header("Overview")
    st.write(
        "- **Purpose:** Predict each player's expected performance (effective runs/wickets) using ML and LSTM forecasting.\n"
        "- **Who benefits:** selectors, analysts, fantasy players, recruiters reviewing your portfolio.\n"
        "- Click **Open Player Profile** to start — pick any player and get a full, focused view."
    )
    st.write("")
    if st.button("Open Player Profile", key="open_profile"):
        # set query param and rerun safely
        set_page_query_param("page", "Player_Profile")
        safe_rerun()

with right:
    st.header("Quick links")
    # links are simple - Streamlit routing may vary; these are friendly anchors
    st.markdown(
        "- [Player Profile](/Player_Profile)\n"
        "- [Batsman Prediction](/Batsman_Prediction)\n"
        "- [Bowler Prediction](/Bowler_Prediction)"
    )

st.write("---")
st.markdown("<div class='card'>"
            "<strong>How to use</strong><br>"
            "1. Open Player Profile → choose player → overview & recent matches.<br>"
            "2. Use auto-filled inputs (from last-5) or enter custom values and click Predict.<br>"
            "3. If LSTM forecasts exist, view next-5 match trend and download CSV."
            "</div>",
            unsafe_allow_html=True)

st.write("")
st.caption("If you want a bolder visual style, tell me which colors or layout you like and I’ll adapt.")
