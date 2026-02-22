"""HRV visualization: metrics bar chart, spectral power."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from config import COLORS, FIGURE_DPI, FIGURE_FORMAT


def plot_hrv_summary(hrv_metrics: dict, output_path: Path,
                     title: str = "HRV Metrics") -> Path:
    """Plot time-domain HRV metrics as horizontal bar chart."""
    td = hrv_metrics.get("time_domain", {})
    if "error" in td:
        return _empty_plot(output_path, td["error"])

    metrics = {
        "RMSSD": td.get("RMSSD_ms"),
        "SDNN": td.get("SDNN_ms"),
        "pNN50 (%)": td.get("pNN50_pct"),
        "Mean HR": td.get("MeanHR_bpm"),
    }
    metrics = {k: v for k, v in metrics.items() if v is not None}

    if not metrics:
        return _empty_plot(output_path, "No HRV metrics available")

    fig, ax = plt.subplots(figsize=(8, 4))
    names = list(metrics.keys())
    values = list(metrics.values())
    colors = [COLORS["hrv_rmssd"], COLORS["ecg_signal"],
              COLORS["accent"], COLORS["heart_rate"]][:len(names)]

    bars = ax.barh(names, values, color=colors, edgecolor="white", height=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", fontsize=10)

    ax.set_xlabel("Value")
    ax.set_title(title)
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path


def plot_hrv_comparison(ecg_rmssd: list[float], oura_rmssd: list[float],
                        dates: list[str], output_path: Path,
                        title: str = "HRV Comparison: ECG vs Oura") -> Path:
    """Plot ECG RMSSD vs Oura RMSSD side by side."""
    if not ecg_rmssd or not oura_rmssd:
        return _empty_plot(output_path, "Insufficient data for HRV comparison")

    n = min(len(ecg_rmssd), len(oura_rmssd), len(dates))
    x = np.arange(n)
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width / 2, ecg_rmssd[:n], width, label="ECG RMSSD",
           color=COLORS["ecg_signal"], alpha=0.8)
    ax.bar(x + width / 2, oura_rmssd[:n], width, label="Oura RMSSD",
           color=COLORS["hrv_rmssd"], alpha=0.8)

    ax.set_xlabel("Date")
    ax.set_ylabel("RMSSD (ms)")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(dates[:n], rotation=45, ha="right", fontsize=8)
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path


def _empty_plot(output_path: Path, message: str) -> Path:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=14,
            color=COLORS["neutral"])
    ax.axis("off")
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path
