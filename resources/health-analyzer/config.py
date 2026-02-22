"""Configuration for Health Data Analyzer."""
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

# --- ECG Settings ---
ECG_SAMPLE_RATE = 512  # Apple Watch samples at 512 Hz
ECG_DURATION_SECONDS = 30
ECG_LEAD = "Lead I"

# R-peak detection method (py-ecg-detectors)
# Options: hamilton, christov, engzee, pan_tompkins, two_average, matched_filter, swt, wqrs
RPEAK_DETECTOR = "hamilton"

# Minimum R-peaks for meaningful HRV computation
HRV_MIN_BEATS = 20

# HRV frequency bands (Hz)
HRV_FREQUENCY_BANDS = {
    "ULF": (0.0, 0.003),
    "VLF": (0.003, 0.04),
    "LF": (0.04, 0.15),
    "HF": (0.15, 0.4),
}

# --- Oura Settings ---
OURA_INTERVAL_SECONDS = 300  # 5-minute intervals for HR/HRV
SLEEP_STAGE_MAP = {
    "1": "deep",
    "2": "light",
    "3": "rem",
    "4": "awake",
}

# --- Visualization ---
FIGURE_DPI = 150
FIGURE_FORMAT = "png"
COLORS = {
    "ecg_signal": "#2196F3",
    "r_peaks": "#F44336",
    "hrv_rmssd": "#4CAF50",
    "sleep_deep": "#1A237E",
    "sleep_light": "#5C6BC0",
    "sleep_rem": "#7E57C2",
    "sleep_awake": "#EF5350",
    "heart_rate": "#FF5722",
    "temperature": "#FF9800",
    "readiness": "#4CAF50",
    "neutral": "#607D8B",
    "accent": "#00BCD4",
}

# --- Report ---
REPORT_PREFIX = "health-report"
MEDICAL_DISCLAIMER = (
    "This analysis is informational only, not medical advice. "
    "Abnormal findings should be discussed with a physician."
)
