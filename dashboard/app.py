# ==========================================
# 🏏 Player Performance Forecast App (LSTM)
# ==========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

# --- 1️⃣ Page Setup ---
st.set_page_config(page_title="Player Performance Forecasts", layout="wide")
st.title("🏏 Cricket Player Performance Forecast Dashboard")
st.markdown("Analyze **batsmen and bowlers** forecasted performances for upcoming matches using LSTM predictions.")

# --- 2️⃣ Load Data ---
@st.cache_data
def load_data():
    batsman_df = pd.read_csv("outputs/batsman_forecast_form.csv")
    bowler_df  = pd.read_csv("outputs/bowler_forecast_form.csv")
    return batsman_df, bowler_df

try:
    batsman_df, bowler_df = load_data()
    st.success("✅ Forecast CSVs loaded successfully!")
except FileNotFoundError:
    st.error("❌ Forecast files not found! Please ensure the files exist in the 'outputs' folder:")
    st.code("outputs/batsman_forecast_form.csv\noutputs/bowler_forecast_form.csv")
    st.stop()

# --- 3️⃣ Sidebar Filters ---
st.sidebar.header("🎯 Select Player Type")
player_type = st.sidebar.radio("Choose Player Type:", ["Batsman", "Bowler"])

if player_type == "Batsman":
    player = st.sidebar.selectbox("Select Batsman", batsman_df['batsman'].unique())
    df_player = batsman_df[batsman_df['batsman'] == player].reset_index(drop=True)
else:
    player = st.sidebar.selectbox("Select Bowler", bowler_df['bowler'].unique())
    df_player = bowler_df[bowler_df['bowler'] == player].reset_index(drop=True)

# --- 4️⃣ Player Forecast Table ---
st.subheader(f"📊 {player} — Forecast Overview")

if player_type == "Batsman":
    display_df = df_player[['forecasted_runs', 'form_status']].copy()
    display_df.columns = ['Forecasted Runs', 'Form Status']
else:
    display_df = df_player[['forecasted_wickets', 'form_status']].copy()
    display_df.columns = ['Forecasted Wickets', 'Form Status']

st.dataframe(display_df, use_container_width=True)

# --- 5️⃣ Forecast Visualization ---
st.subheader(f"📈 {player} — Forecast Trend")

plt.figure(figsize=(8,4))
if player_type == "Batsman":
    plt.plot(df_player['forecasted_runs'], marker='o', color='orange', label="Forecasted Runs")
    plt.ylabel("Runs")
else:
    plt.plot(df_player['forecasted_wickets'], marker='o', color='teal', label="Forecasted Wickets")
    plt.ylabel("Wickets")

plt.title(f"{player} — Next Matches Forecast")
plt.xlabel("Match Number")
plt.xticks(range(len(df_player)), [f"M{i+1}" for i in range(len(df_player))])
plt.legend()
plt.tight_layout()
st.pyplot(plt)

# --- 6️⃣ Next 5 Match Predictions (Cards) ---
st.subheader("🏆 Next 5 Match Predictions")

if player_type == "Batsman":
    forecast_values = df_player['forecasted_runs'].tail(5).values
    label = "Runs"
else:
    forecast_values = df_player['forecasted_wickets'].tail(5).values
    label = "Wickets"

cols = st.columns(min(5, len(forecast_values)))
for i, val in enumerate(forecast_values):
    with cols[i]:
        st.metric(label=f"Match {len(df_player)-len(forecast_values)+i+1}", value=f"{val:.1f} {label}")

# --- 7️⃣ Form Status Distribution ---
st.subheader("🔥 Overall Form Distribution")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Batsman Form Distribution**")
    fig, ax = plt.subplots(figsize=(5,3))
    sns.countplot(data=batsman_df, x='form_status', palette='Set2', ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Count")
    st.pyplot(fig)

with col2:
    st.markdown("**Bowler Form Distribution**")
    fig, ax = plt.subplots(figsize=(5,3))
    sns.countplot(data=bowler_df, x='form_status', palette='Set3', ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# --- 8️⃣ Downloads ---
st.markdown("---")
st.subheader("💾 Download Forecast Data")
st.download_button("⬇️ Download Batsman Forecasts", batsman_df.to_csv(index=False), "batsman_forecast.csv", "text/csv")
st.download_button("⬇️ Download Bowler Forecasts", bowler_df.to_csv(index=False), "bowler_forecast.csv", "text/csv")

# --- Footer ---
st.markdown("---")
st.caption("📘 **Note:** This dashboard visualizes forecasted player performances using LSTM-based models. Built for analytics and portfolio showcase.")
