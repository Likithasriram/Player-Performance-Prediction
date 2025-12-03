# Scripts/predict_module.py
"""
Robust predict_module used by the Streamlit UI.

Behavior:
- Attempts to lazily load model + scaler files from ../models/
- If files are missing or loading fails, uses a safe heuristic fallback
  so the UI buttons continue to work instead of crashing.
"""

import os
from pathlib import Path
import numpy as np
from joblib import load

# Determine project root (one level up from this file's folder)
MODULE_PATH = Path(__file__).resolve()
PROJECT_ROOT = MODULE_PATH.parents[1]   # e.g. project_root/
MODELS_DIR = PROJECT_ROOT / "models"

# Expected model paths
BATSMAN_MODEL_PATH = MODELS_DIR / "batsman_model.pkl"
BATSMAN_SCALER_PATH = MODELS_DIR / "batsman_scaler.pkl"
BOWLER_MODEL_PATH = MODELS_DIR / "bowler_model.pkl"
BOWLER_SCALER_PATH = MODELS_DIR / "bowler_scaler.pkl"

# internal caches
_batsman_model = None
_batsman_scaler = None
_bowler_model = None
_bowler_scaler = None

def _file_exists(p: Path) -> bool:
    try:
        return p.exists()
    except Exception:
        return False

def _try_load(path: Path):
    """Load a joblib file, returning None on failure."""
    try:
        return load(path)
    except Exception:
        return None

def _ensure_batsman_loaded():
    """Load batsman model & scaler into module cache if available."""
    global _batsman_model, _batsman_scaler
    if _batsman_model is not None and _batsman_scaler is not None:
        return True
    if not (_file_exists(BATSMAN_MODEL_PATH) and _file_exists(BATSMAN_SCALER_PATH)):
        return False
    m = _try_load(BATSMAN_MODEL_PATH)
    s = _try_load(BATSMAN_SCALER_PATH)
    if m is None or s is None:
        return False
    _batsman_model, _batsman_scaler = m, s
    return True

def _ensure_bowler_loaded():
    """Load bowler model & scaler into module cache if available."""
    global _bowler_model, _bowler_scaler
    if _bowler_model is not None and _bowler_scaler is not None:
        return True
    if not (_file_exists(BOWLER_MODEL_PATH) and _file_exists(BOWLER_SCALER_PATH)):
        return False
    m = _try_load(BOWLER_MODEL_PATH)
    s = _try_load(BOWLER_SCALER_PATH)
    if m is None or s is None:
        return False
    _bowler_model, _bowler_scaler = m, s
    return True

# ---------------------------
# Public API: prediction functions
# ---------------------------

def predict_batsman(balls_faced, strike_rate, dot_ball_pct):
    """
    Predict effective runs for a batsman.
    If model+scaler are available they are used; otherwise a heuristic fallback is returned.
    """
    # validate numeric inputs
    try:
        bf = float(balls_faced)
        sr = float(strike_rate)
        dot = float(dot_ball_pct)
    except Exception:
        raise ValueError("predict_batsman: inputs must be numeric (balls_faced, strike_rate, dot_ball_pct)")

    # try to use the trained model if available
    if _ensure_batsman_loaded():
        try:
            X = np.array([[bf, sr, dot]])
            Xs = _batsman_scaler.transform(X)
            pred = _batsman_model.predict(Xs)[0]
            return float(pred)
        except Exception:
            # fallback to heuristic on any runtime error
            pass

    # heuristic fallback (safe)
    small_adjust = 0.95
    pred = bf * (sr / 100.0) * (1.0 - dot / 100.0) * small_adjust
    return float(max(0.0, pred))


def predict_bowler(overs, economy, dot_ball_pct):
    """
    Predict effective wickets for a bowler.
    If model+scaler are available they are used; otherwise a heuristic fallback is returned.
    """
    # validate numeric inputs
    try:
        o = float(overs)
        eco = float(economy)
        dot = float(dot_ball_pct)
    except Exception:
        raise ValueError("predict_bowler: inputs must be numeric (overs, economy, dot_ball_pct)")

    # try to use the trained model if available
    if _ensure_bowler_loaded():
        try:
            X = np.array([[o, eco, dot]])
            Xs = _bowler_scaler.transform(X)
            pred = _bowler_model.predict(Xs)[0]
            return float(pred)
        except Exception:
            # fallback to heuristic on any runtime error
            pass

    # heuristic fallback (safe)
    base = o * (dot / 100.0) * 0.6
    penalty = max(0.0, (eco - 6.0) * 0.05)
    pred = max(0.0, base - penalty)
    return float(pred)
