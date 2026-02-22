"""Sleep quality analysis from Oura Ring data."""
import numpy as np
import pandas as pd


def analyze_sleep_night(sleep_row: pd.Series | dict) -> dict:
    """Analyze a single night's sleep data.

    Args:
        sleep_row: One row from Oura sleep DataFrame

    Returns dict with architecture, quality metrics, and HR/HRV during sleep.
    """
    if isinstance(sleep_row, pd.Series):
        s = sleep_row.to_dict()
    else:
        s = dict(sleep_row)

    total = s.get("total_sleep_s", 0) or 0
    deep = s.get("deep_sleep_s", 0) or 0
    light = s.get("light_sleep_s", 0) or 0
    rem = s.get("rem_sleep_s", 0) or 0
    awake = s.get("awake_s", 0) or 0

    total_h = total / 3600
    in_bed_h = (total + awake) / 3600

    architecture = {
        "total_sleep_h": round(total_h, 2),
        "in_bed_h": round(in_bed_h, 2),
        "deep_sleep_h": round(deep / 3600, 2),
        "light_sleep_h": round(light / 3600, 2),
        "rem_sleep_h": round(rem / 3600, 2),
        "awake_h": round(awake / 3600, 2),
        "deep_pct": round(deep / total * 100, 1) if total > 0 else 0,
        "light_pct": round(light / total * 100, 1) if total > 0 else 0,
        "rem_pct": round(rem / total * 100, 1) if total > 0 else 0,
    }

    quality = {
        "efficiency_pct": s.get("efficiency"),
        "latency_min": round(s.get("latency_s", 0) / 60, 1) if s.get("latency_s") else None,
        "score": s.get("score"),
        "restless_periods": s.get("restless_periods"),
    }

    hr_during_sleep = {
        "lowest_hr": s.get("lowest_hr"),
        "average_hr": s.get("average_hr"),
        "average_hrv": s.get("average_hrv"),
        "breath_average": s.get("breath_average"),
        "temperature_delta": s.get("temperature_delta"),
    }

    # Assess against guidelines
    assessment = _assess_architecture(architecture, total_h)

    return {
        "date": str(s.get("date", "unknown")),
        "architecture": architecture,
        "quality": quality,
        "hr_during_sleep": hr_during_sleep,
        "assessment": assessment,
    }


def analyze_sleep_trends(sleep_df: pd.DataFrame, window: int = 7) -> dict:
    """Analyze multi-night sleep trends.

    Args:
        sleep_df: Oura sleep DataFrame
        window: Rolling average window in days

    Returns trend analysis dict.
    """
    if sleep_df.empty or len(sleep_df) < 2:
        return {"error": "Not enough sleep data for trend analysis"}

    df = sleep_df.copy()

    # Convert to hours
    for col in ["total_sleep_s", "deep_sleep_s", "light_sleep_s", "rem_sleep_s"]:
        if col in df.columns:
            df[col.replace("_s", "_h")] = df[col].fillna(0) / 3600

    result = {
        "num_nights": len(df),
        "date_range": [str(df["date"].min()), str(df["date"].max())],
    }

    # Duration trends
    if "total_sleep_h" in df.columns:
        total = df["total_sleep_h"]
        result["duration"] = {
            "mean_h": round(total.mean(), 2),
            "std_h": round(total.std(), 2),
            "min_h": round(total.min(), 2),
            "max_h": round(total.max(), 2),
        }
        if len(total) >= window:
            rolling = total.rolling(window).mean()
            result["duration"]["trend_direction"] = _trend_direction(rolling)
            result["duration"]["rolling_avg_h"] = round(rolling.iloc[-1], 2)

    # Architecture trends
    for stage, col in [("deep", "deep_sleep_h"), ("rem", "rem_sleep_h")]:
        if col in df.columns:
            vals = df[col]
            result[f"{stage}_sleep"] = {
                "mean_h": round(vals.mean(), 2),
                "std_h": round(vals.std(), 2),
            }

    # HRV trends
    if "average_hrv" in df.columns:
        hrv = df["average_hrv"].dropna()
        if len(hrv) >= 2:
            result["hrv_trend"] = {
                "mean_ms": round(hrv.mean(), 1),
                "std_ms": round(hrv.std(), 1),
                "min_ms": round(hrv.min(), 1),
                "max_ms": round(hrv.max(), 1),
            }
            if len(hrv) >= window:
                rolling = hrv.rolling(window).mean()
                result["hrv_trend"]["trend_direction"] = _trend_direction(rolling)

    # Resting HR trends
    if "lowest_hr" in df.columns:
        hr = df["lowest_hr"].dropna()
        if len(hr) >= 2:
            result["resting_hr_trend"] = {
                "mean_bpm": round(hr.mean(), 1),
                "std_bpm": round(hr.std(), 1),
                "min_bpm": round(hr.min(), 1),
                "max_bpm": round(hr.max(), 1),
            }
            if len(hr) >= window:
                rolling = hr.rolling(window).mean()
                result["resting_hr_trend"]["trend_direction"] = _trend_direction(rolling)

    # Efficiency trends
    if "efficiency" in df.columns:
        eff = df["efficiency"].dropna()
        if len(eff) >= 2:
            result["efficiency"] = {
                "mean_pct": round(eff.mean(), 1),
                "min_pct": round(eff.min(), 1),
            }

    # Temperature trends
    if "temperature_delta" in df.columns:
        temp = df["temperature_delta"].dropna()
        if len(temp) >= 2:
            result["temperature"] = {
                "mean_delta": round(temp.mean(), 2),
                "std_delta": round(temp.std(), 2),
                "latest_delta": round(temp.iloc[-1], 2),
            }

    # Bedtime regularity
    if "bedtime_start" in df.columns:
        try:
            bedtimes = pd.to_datetime(df["bedtime_start"])
            hours = bedtimes.dt.hour + bedtimes.dt.minute / 60
            # Handle wraparound (e.g., 23:00 and 00:30 should be close)
            hours = hours.apply(lambda h: h - 24 if h > 18 else h)
            result["regularity"] = {
                "bedtime_std_h": round(hours.std(), 2),
                "regular": hours.std() < 1.0,  # Less than 1 hour std = regular
            }
        except Exception:
            pass

    return result


def _assess_architecture(arch: dict, total_h: float) -> dict:
    """Assess sleep architecture against adult guidelines."""
    notes = []

    if total_h < 6:
        notes.append("Sleep duration below recommended minimum (7-9h)")
    elif total_h < 7:
        notes.append("Sleep duration slightly below recommended (7-9h)")
    elif total_h > 9:
        notes.append("Sleep duration above typical range")

    deep_pct = arch.get("deep_pct", 0)
    if deep_pct < 10:
        notes.append("Deep sleep below typical range (15-25%)")
    elif deep_pct < 15:
        notes.append("Deep sleep slightly below average (15-25%)")

    rem_pct = arch.get("rem_pct", 0)
    if rem_pct < 15:
        notes.append("REM sleep below typical range (20-25%)")

    return {
        "notes": notes,
        "duration_adequate": 7 <= total_h <= 9,
        "architecture_balanced": deep_pct >= 15 and rem_pct >= 20,
    }


def _trend_direction(rolling_series: pd.Series) -> str:
    """Determine trend direction from rolling average."""
    valid = rolling_series.dropna()
    if len(valid) < 3:
        return "insufficient_data"
    recent = valid.iloc[-3:]
    if recent.is_monotonic_increasing:
        return "improving"
    elif recent.is_monotonic_decreasing:
        return "declining"
    return "stable"
