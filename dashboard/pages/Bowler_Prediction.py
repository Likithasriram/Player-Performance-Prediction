import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

import streamlit as st
from Scripts.predict_module import predict_bowler

st.title("🎯 Bowler Performance Prediction")

overs = st.number_input("Overs Bowled", min_value=0.0, value=4.0)
eco = st.number_input("Economy Rate", min_value=0.0, value=7.5)
dot = st.number_input("Dot Ball %", min_value=0.0, max_value=100.0, value=40.0)

if st.button("Predict"):
    pred = predict_bowler(overs, eco, dot)
    st.success(f"Predicted Effective Wickets: {pred:.2f}")
