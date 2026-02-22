"""Cross-device correlation: match ECG recordings with Oura recovery data."""
from datetime import date, timedelta

import numpy as np
import pandas as pd


def correlate_ecg_oura(ecg_analyses: list[dict], oura_data: dict) -> dict:
    """Cross-correlate ECG findings with Oura recovery data.

    Matches ECG recordings to same-day Oura data and computes correlations.

    Args:
        ecg_analyses: List of ECG analysis results (from analyze_ecg_recording)
        oura_data: Parsed Oura data dict with sleep/readiness/activity DataFrames

    Returns correlation analysis dict.
    """
    if not ecg_analyses or oura_data is None:
        return {"error": "Need both ECG and Oura data for cross-correlation"}

    sleep_df = oura_data.get("sleep", pd.DataFrame())
    readiness_df = oura_data.get("readiness", pd.DataFrame())

    # Build ECG date index
    ecg_by_date = {}
    for analysis in ecg_analyses:
        rec = analysis.get("recording", {})
        date_str = rec.get("date", "unknown")
        if date_str == "unknown":
            continue
        try:
            d = pd.to_datetime(date_str).date()
            if d not in ecg_by_date:
                ecg_by_date[d] = []
            ecg_by_date[d].append(analysis)
        except Exception:
            continue

    if not ecg_by_date:
        return {"error": "No ECG recordings with valid dates"}

    # Build Oura date indices
    sleep_by_date = {}
    if not sleep_df.empty and "date" in sleep_df.columns:
        for _, row in sleep_df.iterrows():
            sleep_by_date[row["date"]] = row.to_dict()

    readiness_by_date = {}
    if not readiness_df.empty and "date" in readiness_df.columns:
        for _, row in readiness_df.iterrows():
            readiness_by_date[row["date"]] = row.to_dict()

    # Match days
    matched_days = []
    ecg_hr_values = []
    ecg_rmssd_values = []
    oura_rmssd_values = []
    oura_readiness_values = []

    for ecg_date, ecg_list in sorted(ecg_by_date.items()):
        day_data = {"date": str(ecg_date), "ecg_count": len(ecg_list)}

        # Use first ECG recording of the day for matching
        ecg = ecg_list[0]
        ecg_hr = ecg.get("r_peaks", {}).get("mean_hr_bpm")
        ecg_rr = ecg.get("r_peaks", {}).get("rr_intervals_ms", [])

        day_data["ecg_hr_bpm"] = ecg_hr
        day_data["ecg_classification"] = ecg.get("recording", {}).get("classification")

        # Match sleep data (sleep for the night before or same day)
        sleep = sleep_by_date.get(ecg_date) or sleep_by_date.get(
            ecg_date - timedelta(days=1)
        )
        if sleep:
            day_data["oura_sleep_score"] = sleep.get("score")
            day_data["oura_hrv_ms"] = sleep.get("average_hrv")
            day_data["oura_lowest_hr"] = sleep.get("lowest_hr")
            day_data["oura_efficiency"] = sleep.get("efficiency")

            if sleep.get("average_hrv") is not None:
                oura_rmssd_values.append(sleep["average_hrv"])
                # Compute ECG RMSSD for comparison
                if len(ecg_rr) >= 5:
                    rr = np.array(ecg_rr)
                    rmssd = float(np.sqrt(np.mean(np.diff(rr) ** 2)))
                    ecg_rmssd_values.append(rmssd)
                    day_data["ecg_rmssd_ms"] = round(rmssd, 1)

        # Match readiness
        readiness = readiness_by_date.get(ecg_date)
        if readiness:
            day_data["oura_readiness"] = readiness.get("score")
            if readiness.get("score") is not None:
                oura_readiness_values.append(readiness["score"])
                if ecg_hr is not None:
                    ecg_hr_values.append(ecg_hr)

        matched_days.append(day_data)

    result = {
        "matched_days": matched_days,
        "num_matched": len(matched_days),
        "ecg_date_range": [str(min(ecg_by_date.keys())), str(max(ecg_by_date.keys()))],
    }

    # HRV correlation (ECG RMSSD vs Oura RMSSD)
    if len(ecg_rmssd_values) >= 3 and len(oura_rmssd_values) >= 3:
        min_len = min(len(ecg_rmssd_values), len(oura_rmssd_values))
        ecg_arr = np.array(ecg_rmssd_values[:min_len])
        oura_arr = np.array(oura_rmssd_values[:min_len])

        if np.std(ecg_arr) > 0 and np.std(oura_arr) > 0:
            correlation = np.corrcoef(ecg_arr, oura_arr)[0, 1]
        else:
            correlation = None

        result["hrv_correlation"] = {
            "ecg_rmssd_values": [round(v, 1) for v in ecg_rmssd_values],
            "oura_rmssd_values": [round(v, 1) for v in oura_rmssd_values],
            "pearson_r": round(correlation, 3) if correlation is not None else None,
            "mean_ecg_rmssd": round(np.mean(ecg_arr), 1),
            "mean_oura_rmssd": round(np.mean(oura_arr), 1),
            "mean_difference_ms": round(np.mean(ecg_arr - oura_arr), 1),
            "note": (
                "ECG RMSSD is from a 30-second daytime snapshot. "
                "Oura RMSSD is overnight PPG average. "
                "Systematic differences are expected."
            ),
        }

    # Readiness vs ECG HR correlation
    if len(ecg_hr_values) >= 3 and len(oura_readiness_values) >= 3:
        min_len = min(len(ecg_hr_values), len(oura_readiness_values))
        hr_arr = np.array(ecg_hr_values[:min_len])
        rd_arr = np.array(oura_readiness_values[:min_len])

        if np.std(hr_arr) > 0 and np.std(rd_arr) > 0:
            corr = np.corrcoef(hr_arr, rd_arr)[0, 1]
        else:
            corr = None

        result["readiness_hr_correlation"] = {
            "pearson_r": round(corr, 3) if corr is not None else None,
            "note": "Negative correlation expected (lower HR = higher readiness)",
        }

    # Generate flags for notable findings
    flags = []
    for day in matched_days:
        cls = day.get("ecg_classification", "")
        if cls and cls != "sinusRhythm":
            flags.append(f"{day['date']}: ECG classification '{cls}' - review recommended")
        readiness = day.get("oura_readiness")
        if readiness is not None and readiness < 60:
            flags.append(f"{day['date']}: Low readiness ({readiness}) - recovery concern")

    result["flags"] = flags

    return result
