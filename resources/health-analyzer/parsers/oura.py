"""Oura Ring data parser.

Handles both JSON exports (from Oura web dashboard) and CSV exports.
Oura provides PPG-based metrics: HRV, heart rate, sleep stages, temperature,
readiness scores, and activity data. No ECG - all optical PPG.

JSON structure: { "sleep": [...], "readiness": [...], "activity": [...] }
Each array contains daily summary objects with nested time-series data.
"""
import json
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


def _seconds_to_hours(seconds: float | None) -> float | None:
    """Convert seconds to hours."""
    if seconds is None or np.isnan(seconds):
        return None
    return round(seconds / 3600, 2)


def _parse_sleep_json(sleep_list: list[dict]) -> pd.DataFrame:
    """Parse sleep array from Oura JSON export."""
    if not sleep_list:
        return pd.DataFrame()

    records = []
    for s in sleep_list:
        rec = {
            "date": s.get("summary_date", s.get("day", "")),
            "bedtime_start": s.get("bedtime_start", ""),
            "bedtime_end": s.get("bedtime_end", ""),
            "total_sleep_s": s.get("total", s.get("total_sleep_duration", 0)),
            "deep_sleep_s": s.get("deep", s.get("deep_sleep_duration", 0)),
            "light_sleep_s": s.get("light", s.get("light_sleep_duration", 0)),
            "rem_sleep_s": s.get("rem", s.get("rem_sleep_duration", 0)),
            "awake_s": s.get("awake", s.get("awake_time", 0)),
            "efficiency": s.get("efficiency", s.get("sleep_efficiency", None)),
            "latency_s": s.get("onset_latency", s.get("latency", 0)),
            "score": s.get("score", s.get("sleep_score", None)),
            "lowest_hr": s.get("lowest_heart_rate", s.get("hr_lowest", None)),
            "average_hr": s.get("average_heart_rate", s.get("hr_average", None)),
            "average_hrv": s.get("average_hrv", None),
            "breath_average": s.get("breath_average", s.get("average_breath", None)),
            "temperature_delta": s.get("temperature_delta",
                                       s.get("temperature_deviation", None)),
            "restless_periods": s.get("restless_periods", s.get("restless", None)),
        }

        # Extract 5-minute HR time-series if present
        hr_data = s.get("hr", s.get("heart_rate", {}))
        if isinstance(hr_data, dict) and "items" in hr_data:
            rec["hr_5min"] = hr_data["items"]
            rec["hr_interval"] = hr_data.get("interval", 300)
        elif isinstance(hr_data, list):
            rec["hr_5min"] = hr_data
            rec["hr_interval"] = 300

        # Extract 5-minute HRV time-series if present
        hrv_data = s.get("hrv", s.get("heart_rate_variability", {}))
        if isinstance(hrv_data, dict) and "items" in hrv_data:
            rec["hrv_5min"] = hrv_data["items"]
            rec["hrv_interval"] = hrv_data.get("interval", 300)
        elif isinstance(hrv_data, list):
            rec["hrv_5min"] = hrv_data
            rec["hrv_interval"] = 300

        records.append(rec)

    df = pd.DataFrame(records)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df = df.sort_values("date").reset_index(drop=True)
    return df


def _parse_readiness_json(readiness_list: list[dict]) -> pd.DataFrame:
    """Parse readiness array from Oura JSON export."""
    if not readiness_list:
        return pd.DataFrame()

    records = []
    for r in readiness_list:
        rec = {
            "date": r.get("summary_date", r.get("day", "")),
            "score": r.get("score", None),
            "score_activity_balance": r.get("score_activity_balance", None),
            "score_previous_day": r.get("score_previous_day_activity",
                                        r.get("score_previous_day", None)),
            "score_previous_night": r.get("score_previous_night", None),
            "score_recovery_index": r.get("score_recovery_index", None),
            "score_resting_hr": r.get("score_resting_hr", None),
            "score_sleep_balance": r.get("score_sleep_balance", None),
            "score_temperature": r.get("score_temperature", None),
            "score_hrv_balance": r.get("score_hrv_balance", None),
        }
        records.append(rec)

    df = pd.DataFrame(records)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df = df.sort_values("date").reset_index(drop=True)
    return df


def _parse_activity_json(activity_list: list[dict]) -> pd.DataFrame:
    """Parse activity array from Oura JSON export."""
    if not activity_list:
        return pd.DataFrame()

    records = []
    for a in activity_list:
        rec = {
            "date": a.get("summary_date", a.get("day", "")),
            "score": a.get("score", None),
            "steps": a.get("steps", a.get("daily_movement", 0)),
            "cal_active": a.get("cal_active", a.get("active_calories", 0)),
            "cal_total": a.get("cal_total", a.get("total_calories", 0)),
            "high_activity_s": a.get("high", 0),
            "medium_activity_s": a.get("medium", 0),
            "low_activity_s": a.get("low", 0),
            "inactive_s": a.get("inactive", a.get("sedentary_time", 0)),
            "rest_s": a.get("rest", 0),
            "average_met": a.get("average_met", a.get("met", {}).get("average", None)),
        }
        records.append(rec)

    df = pd.DataFrame(records)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df = df.sort_values("date").reset_index(drop=True)
    return df


def parse_oura_json(filepath: Path) -> dict:
    """Parse Oura Ring JSON export.

    Returns dict with keys:
        sleep (DataFrame), readiness (DataFrame), activity (DataFrame),
        date_range (tuple), num_nights (int)
    """
    filepath = Path(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    sleep_df = _parse_sleep_json(data.get("sleep", []))
    readiness_df = _parse_readiness_json(data.get("readiness", []))
    activity_df = _parse_activity_json(data.get("activity", []))

    # Determine date range across all data
    all_dates = []
    for df in [sleep_df, readiness_df, activity_df]:
        if not df.empty and "date" in df.columns:
            all_dates.extend(df["date"].tolist())

    date_range = (min(all_dates), max(all_dates)) if all_dates else (None, None)

    return {
        "sleep": sleep_df,
        "readiness": readiness_df,
        "activity": activity_df,
        "date_range": date_range,
        "num_nights": len(sleep_df),
        "source": str(filepath),
    }


def parse_oura_csv(dirpath: Path) -> dict:
    """Parse Oura CSV export (one or more CSV files in a directory).

    Oura CSV exports may have separate files for sleep, readiness, activity,
    or a single combined file.
    """
    dirpath = Path(dirpath)

    result = {
        "sleep": pd.DataFrame(),
        "readiness": pd.DataFrame(),
        "activity": pd.DataFrame(),
        "date_range": (None, None),
        "num_nights": 0,
        "source": str(dirpath),
    }

    csv_files = list(dirpath.glob("*.csv"))

    for csv_file in csv_files:
        name_lower = csv_file.stem.lower()
        try:
            df = pd.read_csv(csv_file)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.date
            elif "summary_date" in df.columns:
                df["date"] = pd.to_datetime(df["summary_date"]).dt.date

            if "sleep" in name_lower:
                result["sleep"] = df
            elif "readiness" in name_lower:
                result["readiness"] = df
            elif "activity" in name_lower:
                result["activity"] = df
            else:
                # Try to detect by columns
                cols = set(df.columns)
                if {"deep", "light", "rem"} & cols or {"total_sleep_duration"} & cols:
                    result["sleep"] = df
                elif {"score_activity_balance", "score_recovery_index"} & cols:
                    result["readiness"] = df
                elif {"steps", "cal_active"} & cols:
                    result["activity"] = df
        except Exception as e:
            print(f"Warning: Failed to parse Oura CSV {csv_file.name}: {e}")

    all_dates = []
    for key in ["sleep", "readiness", "activity"]:
        df = result[key]
        if not df.empty and "date" in df.columns:
            all_dates.extend(df["date"].tolist())

    result["date_range"] = (min(all_dates), max(all_dates)) if all_dates else (None, None)
    result["num_nights"] = len(result["sleep"])
    return result


def detect_oura_format(path: Path) -> str:
    """Auto-detect whether path is a JSON file or CSV directory.

    Returns: 'json', 'csv', or 'unknown'
    """
    path = Path(path)
    if path.is_file() and path.suffix.lower() == ".json":
        return "json"
    if path.is_dir():
        csv_files = list(path.glob("*.csv"))
        if csv_files:
            return "csv"
    if path.is_file() and path.suffix.lower() == ".csv":
        return "csv"
    return "unknown"


def parse_oura_auto(path: Path) -> dict:
    """Auto-detect format and parse Oura data."""
    fmt = detect_oura_format(path)
    if fmt == "json":
        return parse_oura_json(path)
    elif fmt == "csv":
        if path.is_dir():
            return parse_oura_csv(path)
        else:
            # Single CSV file - wrap in directory parse
            return parse_oura_csv(path.parent)
    else:
        raise ValueError(f"Cannot detect Oura data format at: {path}")


def find_oura_data(data_dir: Path) -> dict | None:
    """Auto-detect and parse Oura data from the data directory.

    Looks for:
    - *.json files that contain Oura data structures
    - oura/ subdirectory with CSV files
    - CSV files with oura-like naming
    """
    data_dir = Path(data_dir)

    # Check JSON files
    for jf in sorted(data_dir.glob("*.json")):
        try:
            with open(jf) as f:
                data = json.load(f)
            # Detect if it's Oura data by checking for expected keys
            if any(k in data for k in ["sleep", "readiness", "activity"]):
                return parse_oura_json(jf)
        except (json.JSONDecodeError, Exception):
            continue

    # Check for oura/ subdirectory
    oura_dir = data_dir / "oura"
    if oura_dir.is_dir():
        return parse_oura_csv(oura_dir)

    # Check for Oura-like CSV files
    oura_csvs = [f for f in data_dir.glob("*.csv") if "oura" in f.stem.lower()]
    if oura_csvs:
        return parse_oura_csv(data_dir)

    return None
