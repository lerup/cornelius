"""Recovery and readiness analysis from Oura Ring data."""
import numpy as np
import pandas as pd


def analyze_readiness(readiness_df: pd.DataFrame) -> dict:
    """Analyze readiness trends and component scores.

    Args:
        readiness_df: Oura readiness DataFrame

    Returns readiness analysis dict.
    """
    if readiness_df.empty:
        return {"error": "No readiness data available"}

    df = readiness_df.copy()
    result = {
        "num_days": len(df),
        "date_range": [str(df["date"].min()), str(df["date"].max())],
    }

    # Overall score
    score = df["score"].dropna()
    if len(score) >= 1:
        result["score"] = {
            "latest": int(score.iloc[-1]),
            "mean": round(score.mean(), 1),
            "std": round(score.std(), 1),
            "min": int(score.min()),
            "max": int(score.max()),
        }
        result["score"]["category"] = _readiness_category(score.iloc[-1])

        if len(score) >= 7:
            rolling = score.rolling(7).mean()
            result["score"]["trend_7d"] = _trend_direction(rolling)

    # Component breakdown (latest day)
    latest = df.iloc[-1].to_dict()
    components = {}
    component_cols = [
        ("score_activity_balance", "Activity Balance"),
        ("score_previous_day", "Previous Day Activity"),
        ("score_previous_night", "Previous Night Sleep"),
        ("score_recovery_index", "Recovery Index"),
        ("score_resting_hr", "Resting Heart Rate"),
        ("score_sleep_balance", "Sleep Balance"),
        ("score_temperature", "Temperature"),
        ("score_hrv_balance", "HRV Balance"),
    ]
    for col, label in component_cols:
        val = latest.get(col)
        if val is not None and not (isinstance(val, float) and np.isnan(val)):
            components[label] = int(val)

    if components:
        result["components"] = components
        # Identify weakest components
        sorted_comps = sorted(components.items(), key=lambda x: x[1])
        result["weakest"] = [
            {"component": name, "score": val}
            for name, val in sorted_comps[:3]
            if val < 80
        ]

    return result


def analyze_temperature(sleep_df: pd.DataFrame) -> dict:
    """Analyze temperature deviation patterns from Oura sleep data.

    Temperature delta measures deviation from personal baseline.
    Elevated temperature may indicate illness, overtraining, or hormonal changes.
    """
    if sleep_df.empty or "temperature_delta" not in sleep_df.columns:
        return {"error": "No temperature data available"}

    temp = sleep_df[["date", "temperature_delta"]].dropna(subset=["temperature_delta"])
    if temp.empty:
        return {"error": "No temperature data available"}

    vals = temp["temperature_delta"]
    result = {
        "num_days": len(temp),
        "mean_delta": round(vals.mean(), 2),
        "std_delta": round(vals.std(), 2),
        "latest_delta": round(vals.iloc[-1], 2),
        "max_delta": round(vals.max(), 2),
        "min_delta": round(vals.min(), 2),
    }

    # Elevated temperature detection
    threshold = 0.5  # degrees above baseline
    elevated_days = temp[vals > threshold]
    if not elevated_days.empty:
        result["elevated_days"] = [
            {"date": str(row["date"]), "delta": round(row["temperature_delta"], 2)}
            for _, row in elevated_days.iterrows()
        ]
        result["elevated_flag"] = True
    else:
        result["elevated_flag"] = False

    # Trend
    if len(vals) >= 7:
        rolling = vals.rolling(7).mean()
        result["trend_7d"] = _trend_direction(rolling)

    return result


def compute_recovery_trajectory(readiness_df: pd.DataFrame,
                                 sleep_df: pd.DataFrame) -> dict:
    """Compute overall recovery trajectory combining readiness + sleep signals.

    Returns trajectory assessment: improving, stable, declining, or mixed.
    """
    signals = {}

    # Readiness trend
    if not readiness_df.empty and "score" in readiness_df.columns:
        score = readiness_df["score"].dropna()
        if len(score) >= 7:
            rolling = score.rolling(7).mean().dropna()
            if len(rolling) >= 3:
                signals["readiness"] = _slope_direction(rolling)

    # HRV trend (higher = better recovery)
    if not sleep_df.empty and "average_hrv" in sleep_df.columns:
        hrv = sleep_df["average_hrv"].dropna()
        if len(hrv) >= 7:
            rolling = hrv.rolling(7).mean().dropna()
            if len(rolling) >= 3:
                signals["hrv"] = _slope_direction(rolling)

    # Resting HR trend (lower = better recovery)
    if not sleep_df.empty and "lowest_hr" in sleep_df.columns:
        hr = sleep_df["lowest_hr"].dropna()
        if len(hr) >= 7:
            rolling = hr.rolling(7).mean().dropna()
            if len(rolling) >= 3:
                # Invert: declining HR = improving recovery
                hr_dir = _slope_direction(rolling)
                signals["resting_hr"] = {
                    "improving": "declining",
                    "declining": "improving",
                    "stable": "stable",
                }.get(hr_dir, hr_dir)

    if not signals:
        return {"trajectory": "insufficient_data", "signals": {}}

    # Aggregate: majority vote
    directions = list(signals.values())
    improving = directions.count("improving")
    declining = directions.count("declining")
    stable = directions.count("stable")

    if improving > declining and improving > stable:
        trajectory = "improving"
    elif declining > improving and declining > stable:
        trajectory = "declining"
    elif improving == declining and improving > 0:
        trajectory = "mixed"
    else:
        trajectory = "stable"

    return {
        "trajectory": trajectory,
        "signals": signals,
        "confidence": max(improving, declining, stable) / len(directions),
    }


def _readiness_category(score: float) -> str:
    if score >= 85:
        return "excellent"
    elif score >= 70:
        return "good"
    elif score >= 60:
        return "fair"
    return "pay_attention"


def _trend_direction(rolling_series: pd.Series) -> str:
    valid = rolling_series.dropna()
    if len(valid) < 3:
        return "insufficient_data"
    recent = valid.iloc[-3:]
    if recent.is_monotonic_increasing:
        return "improving"
    elif recent.is_monotonic_decreasing:
        return "declining"
    return "stable"


def _slope_direction(series: pd.Series) -> str:
    """Determine direction from linear slope of recent values."""
    recent = series.iloc[-7:] if len(series) >= 7 else series
    x = np.arange(len(recent))
    if len(x) < 3:
        return "stable"
    slope = np.polyfit(x, recent.values, 1)[0]
    threshold = recent.std() * 0.1 if recent.std() > 0 else 0.01
    if slope > threshold:
        return "improving"
    elif slope < -threshold:
        return "declining"
    return "stable"
