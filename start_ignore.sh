#!/usr/bin/env bash
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_PORT=${PORT:-8501}
streamlit run dashboard/Home.py --server.port $STREAMLIT_SERVER_PORT --server.address 0.0.0.0
