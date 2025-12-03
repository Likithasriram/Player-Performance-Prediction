import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

import streamlit as st
from Scripts.predict_module import predict_batsman

st.title("🏏 Batsman Performance Prediction")

balls = st.number_input("Balls faced", min_value=0, value=30)
sr = st.number_input("Strike Rate", min_value=0.0, value=150.0)
dot = st.number_input("Dot Ball %", min_value=0.0, max_value=100.0, value=25.0)

if st.button("Predict"):
    pred = predict_batsman(balls, sr, dot)
    st.success(f"Predicted Effective Runs: {pred:.2f}")
