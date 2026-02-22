"""HRV analysis: time-domain, frequency-domain, and nonlinear metrics."""
import numpy as np

try:
    import neurokit2 as nk
except ImportError:
    nk = None


def compute_hrv_from_rr(rr_intervals_ms: np.ndarray, sample_rate: int = 512) -> dict:
    """Compute comprehensive HRV metrics from RR intervals.

    Args:
        rr_intervals_ms: Array of RR intervals in milliseconds
        sample_rate: Original ECG sample rate (for frequency analysis)

    Returns dict with time_domain, frequency_domain, nonlinear sub-dicts.
    """
    if len(rr_intervals_ms) < 5:
        return _empty_hrv("Too few beats for HRV analysis")

    rr = np.array(rr_intervals_ms, dtype=np.float64)

    # --- Time Domain (computed directly) ---
    mean_nn = float(np.mean(rr))
    sdnn = float(np.std(rr, ddof=1))
    successive_diffs = np.diff(rr)
    rmssd = float(np.sqrt(np.mean(successive_diffs ** 2)))
    sdsd = float(np.std(successive_diffs, ddof=1))
    nn50 = int(np.sum(np.abs(successive_diffs) > 50))
    pnn50 = (nn50 / len(successive_diffs)) * 100 if len(successive_diffs) > 0 else 0
    mean_hr = 60000 / mean_nn if mean_nn > 0 else None

    time_domain = {
        "MeanNN_ms": round(mean_nn, 1),
        "SDNN_ms": round(sdnn, 1),
        "RMSSD_ms": round(rmssd, 1),
        "SDSD_ms": round(sdsd, 1),
        "pNN50_pct": round(pnn50, 1),
        "NN50": nn50,
        "MeanHR_bpm": round(mean_hr, 1) if mean_hr else None,
    }

    # --- Frequency Domain (via NeuroKit2 if available) ---
    frequency_domain = {}
    if nk is not None and len(rr) >= 10:
        try:
            # Create R-peak positions from RR intervals
            r_peaks_samples = np.cumsum(np.concatenate([[0], rr / 1000 * sample_rate])).astype(int)
            hrv_freq = nk.hrv_frequency({"ECG_R_Peaks": r_peaks_samples},
                                        sampling_rate=sample_rate)
            frequency_domain = {
                "VLF_ms2": _safe_float(hrv_freq.get("HRV_VLF", None)),
                "LF_ms2": _safe_float(hrv_freq.get("HRV_LF", None)),
                "HF_ms2": _safe_float(hrv_freq.get("HRV_HF", None)),
                "LF_HF_ratio": _safe_float(hrv_freq.get("HRV_LFHF", None)),
                "LF_norm": _safe_float(hrv_freq.get("HRV_LFn", None)),
                "HF_norm": _safe_float(hrv_freq.get("HRV_HFn", None)),
            }
        except Exception:
            frequency_domain = {"error": "Frequency analysis failed - recording too short"}

    # --- Nonlinear (Poincare) ---
    nonlinear = {}
    if len(rr) >= 5:
        rr_n = rr[:-1]
        rr_n1 = rr[1:]
        sd1 = float(np.std(rr_n1 - rr_n, ddof=1) / np.sqrt(2))
        sd2 = float(np.std(rr_n1 + rr_n, ddof=1) / np.sqrt(2))
        nonlinear = {
            "SD1_ms": round(sd1, 1),
            "SD2_ms": round(sd2, 1),
            "SD1_SD2_ratio": round(sd1 / sd2, 3) if sd2 > 0 else None,
        }

        # Sample entropy (via NeuroKit2 if available)
        if nk is not None:
            try:
                sampen = nk.entropy_sample(rr)
                nonlinear["SampEn"] = round(float(sampen), 3) if sampen else None
            except Exception:
                pass

    return {
        "time_domain": time_domain,
        "frequency_domain": frequency_domain,
        "nonlinear": nonlinear,
    }


def compute_hrv_from_oura(sleep_row: dict) -> dict:
    """Compute HRV summary from a single Oura sleep night.

    Args:
        sleep_row: A row from the Oura sleep DataFrame (as dict)

    Returns dict with Oura-derived HRV metrics.
    """
    result = {
        "source": "oura_ppg",
        "average_hrv_ms": sleep_row.get("average_hrv"),
        "lowest_hr_bpm": sleep_row.get("lowest_hr"),
        "average_hr_bpm": sleep_row.get("average_hr"),
    }

    # Process 5-minute HRV time-series if available
    hrv_5min = sleep_row.get("hrv_5min")
    if hrv_5min and isinstance(hrv_5min, list):
        values = [v for v in hrv_5min if v is not None and v > 0]
        if values:
            result["hrv_min_ms"] = round(min(values), 1)
            result["hrv_max_ms"] = round(max(values), 1)
            result["hrv_std_ms"] = round(float(np.std(values)), 1)
            result["hrv_median_ms"] = round(float(np.median(values)), 1)
            result["num_intervals"] = len(values)

    return result


def compare_hrv_sources(ecg_hrv: dict, oura_hrv: dict, date_str: str) -> dict:
    """Compare HRV measurements from ECG vs Oura on the same date.

    Returns comparison dict with both values and delta.
    """
    ecg_rmssd = ecg_hrv.get("time_domain", {}).get("RMSSD_ms")
    oura_rmssd = oura_hrv.get("average_hrv_ms")

    comparison = {
        "date": date_str,
        "ecg_rmssd_ms": ecg_rmssd,
        "oura_rmssd_ms": oura_rmssd,
    }

    if ecg_rmssd is not None and oura_rmssd is not None:
        comparison["delta_ms"] = round(ecg_rmssd - oura_rmssd, 1)
        comparison["delta_pct"] = round(
            (ecg_rmssd - oura_rmssd) / oura_rmssd * 100, 1
        ) if oura_rmssd > 0 else None
        comparison["note"] = (
            "ECG captures a 30-second snapshot; Oura averages overnight PPG. "
            "Differences are expected."
        )

    return comparison


def contextualize_hrv(hrv_metrics: dict) -> dict:
    """Add population context to HRV values.

    Returns dict with interpretations for key metrics.
    """
    td = hrv_metrics.get("time_domain", {})
    context = {}

    rmssd = td.get("RMSSD_ms")
    if rmssd is not None:
        if rmssd > 100:
            context["rmssd"] = "High - strong parasympathetic tone"
        elif rmssd > 40:
            context["rmssd"] = "Normal - healthy autonomic balance"
        elif rmssd > 20:
            context["rmssd"] = "Below average - may indicate stress or fatigue"
        else:
            context["rmssd"] = "Low - reduced parasympathetic activity"

    sdnn = td.get("SDNN_ms")
    if sdnn is not None:
        if sdnn > 100:
            context["sdnn"] = "High overall variability"
        elif sdnn > 50:
            context["sdnn"] = "Normal overall variability"
        else:
            context["sdnn"] = "Reduced overall variability"

    pnn50 = td.get("pNN50_pct")
    if pnn50 is not None:
        if pnn50 > 25:
            context["pnn50"] = "High vagal tone"
        elif pnn50 > 5:
            context["pnn50"] = "Normal range"
        else:
            context["pnn50"] = "Low vagal activity"

    lf_hf = hrv_metrics.get("frequency_domain", {}).get("LF_HF_ratio")
    if lf_hf is not None:
        if lf_hf > 3:
            context["lf_hf"] = "Sympathetic dominant"
        elif lf_hf > 1:
            context["lf_hf"] = "Balanced with slight sympathetic lean"
        else:
            context["lf_hf"] = "Parasympathetic dominant"

    return context


def _safe_float(val) -> float | None:
    """Safely extract float from DataFrame cell or scalar."""
    if val is None:
        return None
    try:
        if hasattr(val, "iloc"):
            val = val.iloc[0]
        f = float(val)
        return round(f, 2) if not np.isnan(f) else None
    except (ValueError, TypeError, IndexError):
        return None


def _empty_hrv(reason: str) -> dict:
    return {
        "time_domain": {"error": reason},
        "frequency_domain": {},
        "nonlinear": {},
    }
