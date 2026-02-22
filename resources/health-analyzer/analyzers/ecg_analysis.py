"""ECG waveform analysis: R-peak detection, rhythm analysis, signal quality."""
import numpy as np

try:
    from ecgdetectors import Detectors
except ImportError:
    Detectors = None

try:
    import neurokit2 as nk
except ImportError:
    nk = None


DETECTOR_METHODS = {
    "hamilton": "hamilton_detector",
    "christov": "christov_detector",
    "engzee": "engzee_detector",
    "pan_tompkins": "pan_tompkins_detector",
    "two_average": "two_average_detector",
    "matched_filter": "matched_filter_detector",
    "swt": "swt_detector",
    "wqrs": "wqrs_detector",
}


def detect_r_peaks(voltage_uv: np.ndarray, sample_rate: int = 512,
                   method: str = "hamilton") -> dict:
    """Detect R-peaks in ECG signal using py-ecg-detectors.

    Args:
        voltage_uv: Voltage array in microvolts
        sample_rate: Sampling rate in Hz
        method: Detection algorithm name

    Returns dict with:
        r_peak_indices, r_peak_times_s, num_beats, rr_intervals_ms, mean_hr_bpm
    """
    if Detectors is None:
        raise ImportError("py-ecg-detectors not installed. Run setup.sh first.")

    detectors = Detectors(sample_rate)
    detector_fn = getattr(detectors, DETECTOR_METHODS.get(method, "hamilton_detector"))

    # Convert to millivolts for detector (some algorithms expect mV)
    signal_mv = voltage_uv / 1000.0
    r_peaks = np.array(detector_fn(signal_mv))

    # Filter out invalid peaks
    r_peaks = r_peaks[(r_peaks >= 0) & (r_peaks < len(voltage_uv))]

    if len(r_peaks) < 2:
        return {
            "r_peak_indices": r_peaks,
            "r_peak_times_s": r_peaks / sample_rate,
            "num_beats": len(r_peaks),
            "rr_intervals_ms": np.array([]),
            "mean_hr_bpm": None,
            "method": method,
        }

    r_peak_times = r_peaks / sample_rate
    rr_intervals = np.diff(r_peaks) / sample_rate * 1000  # in milliseconds
    mean_hr = 60000 / np.mean(rr_intervals) if len(rr_intervals) > 0 else None

    return {
        "r_peak_indices": r_peaks,
        "r_peak_times_s": r_peak_times,
        "num_beats": len(r_peaks),
        "rr_intervals_ms": rr_intervals,
        "mean_hr_bpm": round(mean_hr, 1) if mean_hr else None,
        "method": method,
    }


def assess_signal_quality(voltage_uv: np.ndarray, sample_rate: int = 512) -> dict:
    """Assess ECG signal quality using NeuroKit2.

    Returns dict with:
        quality_score (0-1), quality_label, noise_level, baseline_wander
    """
    if nk is None:
        return {
            "quality_score": None,
            "quality_label": "unknown",
            "noise_level": None,
            "baseline_wander": None,
        }

    try:
        signal_mv = voltage_uv / 1000.0
        cleaned = nk.ecg_clean(signal_mv, sampling_rate=sample_rate)

        # Use averageQRS method - returns 0-1 float scores (not string labels)
        # zhao2018 returns strings ("Unacceptable", "Barely acceptable", "Excellent")
        # which can't be averaged numerically
        quality = nk.ecg_quality(cleaned, sampling_rate=sample_rate, method="averageQRS")

        if hasattr(quality, "mean"):
            avg_quality = float(quality.mean())
        elif isinstance(quality, (list, np.ndarray)):
            avg_quality = float(np.mean(quality))
        elif isinstance(quality, str):
            # Fallback: map string labels to numeric scores
            label_map = {
                "excellent": 0.9, "good": 0.7, "barely acceptable": 0.4,
                "unacceptable": 0.1,
            }
            avg_quality = label_map.get(quality.lower(), 0.5)
        else:
            avg_quality = float(quality)

        # Classify
        if avg_quality >= 0.7:
            label = "good"
        elif avg_quality >= 0.4:
            label = "acceptable"
        else:
            label = "poor"

        # Estimate noise level (ratio of high-freq energy)
        from scipy import signal as sig
        freqs, psd = sig.welch(voltage_uv, fs=sample_rate, nperseg=min(256, len(voltage_uv)))
        total_power = np.sum(psd)
        noise_power = np.sum(psd[freqs > 40]) if total_power > 0 else 0
        noise_ratio = noise_power / total_power if total_power > 0 else 0

        # Detect baseline wander (energy below 0.5 Hz)
        wander_power = np.sum(psd[freqs < 0.5])
        baseline_wander = (wander_power / total_power) > 0.3 if total_power > 0 else False

        return {
            "quality_score": round(avg_quality, 3),
            "quality_label": label,
            "noise_level": round(noise_ratio, 3),
            "baseline_wander": bool(baseline_wander),
        }
    except Exception as e:
        return {
            "quality_score": None,
            "quality_label": "error",
            "noise_level": None,
            "baseline_wander": None,
            "error": str(e),
        }


def analyze_rhythm(rr_intervals_ms: np.ndarray) -> dict:
    """Analyze heart rhythm regularity from RR intervals.

    Returns dict with:
        rhythm_regular, cv_rr, premature_beats, irregularity_score
    """
    if len(rr_intervals_ms) < 3:
        return {
            "rhythm_regular": None,
            "cv_rr": None,
            "premature_beats": 0,
            "irregularity_score": None,
        }

    mean_rr = np.mean(rr_intervals_ms)
    std_rr = np.std(rr_intervals_ms)
    cv_rr = std_rr / mean_rr if mean_rr > 0 else 0

    # Detect premature beats: RR interval < 80% of mean
    premature_threshold = mean_rr * 0.80
    premature_beats = int(np.sum(rr_intervals_ms < premature_threshold))

    # Irregularity score: successive RR differences
    successive_diffs = np.abs(np.diff(rr_intervals_ms))
    irregularity = np.mean(successive_diffs) / mean_rr if mean_rr > 0 else 0

    # Regular if CV < 0.10 and few premature beats
    rhythm_regular = cv_rr < 0.10 and premature_beats <= 1

    return {
        "rhythm_regular": rhythm_regular,
        "cv_rr": round(cv_rr, 4),
        "premature_beats": premature_beats,
        "irregularity_score": round(irregularity, 4),
        "mean_rr_ms": round(mean_rr, 1),
        "std_rr_ms": round(std_rr, 1),
    }


def analyze_ecg_recording(ecg_data: dict, method: str = "hamilton") -> dict:
    """Full analysis pipeline for a single ECG recording.

    Args:
        ecg_data: Output from parse_ecg_csv()
        method: R-peak detection algorithm

    Returns comprehensive analysis dict.
    """
    voltage = ecg_data["voltage_uv"]
    sr = ecg_data["sample_rate"]

    if len(voltage) < sr:  # Less than 1 second of data
        return {
            "recording": {
                "date": str(ecg_data["date"]) if ecg_data["date"] else "unknown",
                "classification": ecg_data["classification"],
                "duration_s": ecg_data["duration_s"],
                "num_samples": ecg_data["num_samples"],
            },
            "error": "Recording too short for analysis",
        }

    # Signal quality
    quality = assess_signal_quality(voltage, sr)

    # R-peak detection
    peaks = detect_r_peaks(voltage, sr, method)

    # Rhythm analysis
    rhythm = analyze_rhythm(peaks["rr_intervals_ms"])

    return {
        "recording": {
            "date": str(ecg_data["date"]) if ecg_data["date"] else "unknown",
            "classification": ecg_data["classification"],
            "average_hr_reported": ecg_data["average_hr"],
            "duration_s": round(ecg_data["duration_s"], 1),
            "num_samples": ecg_data["num_samples"],
            "sample_rate": sr,
            "filepath": ecg_data["filepath"],
        },
        "signal_quality": quality,
        "r_peaks": {
            "method": peaks["method"],
            "num_beats": peaks["num_beats"],
            "mean_hr_bpm": peaks["mean_hr_bpm"],
            "rr_intervals_ms": peaks["rr_intervals_ms"].tolist() if len(peaks["rr_intervals_ms"]) > 0 else [],
        },
        "rhythm": rhythm,
        "voltage_uv": voltage,  # Kept for visualization
        "r_peak_indices": peaks["r_peak_indices"],  # Kept for visualization
    }
