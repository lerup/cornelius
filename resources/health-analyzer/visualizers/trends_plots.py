"""Multi-day trend visualization: HR, HRV, readiness, temperature."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import COLORS, FIGURE_DPI, FIGURE_FORMAT


def plot_hr_hrv_trends(sleep_df: pd.DataFrame, output_path: Path,
                       title: str = "Heart Rate & HRV Trends") -> Path:
    """Plot resting HR and HRV trends over time."""
    if sleep_df.empty or len(sleep_df) < 2:
        return _empty_plot(output_path, "Not enough data for trends")

    df = sleep_df.copy()
    dates = df["date"].astype(str)
    has_hr = "lowest_hr" in df.columns and df["lowest_hr"].notna().sum() > 1
    has_hrv = "average_hrv" in df.columns and df["average_hrv"].notna().sum() > 1

    if not has_hr and not has_hrv:
        return _empty_plot(output_path, "No HR/HRV trend data available")

    fig, axes = plt.subplots(2 if (has_hr and has_hrv) else 1, 1,
                              figsize=(12, 8 if (has_hr and has_hrv) else 5),
                              sharex=True)
    if not isinstance(axes, np.ndarray):
        axes = [axes]

    idx = 0

    # Resting HR
    if has_hr:
        hr = df["lowest_hr"].fillna(method="ffill")
        axes[idx].plot(dates, hr, color=COLORS["heart_rate"], marker="o",
                       markersize=3, linewidth=1.5)
        if len(hr) >= 7:
            rolling = hr.rolling(7).mean()
            axes[idx].plot(dates, rolling, color=COLORS["heart_rate"],
                          linestyle="--", linewidth=2, alpha=0.6, label="7-day avg")
        axes[idx].set_ylabel("BPM")
        axes[idx].set_title("Resting Heart Rate (Lowest)")
        axes[idx].legend(fontsize=8)
        axes[idx].grid(True, alpha=0.3)
        axes[idx].invert_yaxis()  # Lower HR = better
        idx += 1

    # HRV
    if has_hrv:
        hrv = df["average_hrv"].fillna(method="ffill")
        axes[idx].plot(dates, hrv, color=COLORS["hrv_rmssd"], marker="o",
                       markersize=3, linewidth=1.5)
        if len(hrv) >= 7:
            rolling = hrv.rolling(7).mean()
            axes[idx].plot(dates, rolling, color=COLORS["hrv_rmssd"],
                          linestyle="--", linewidth=2, alpha=0.6, label="7-day avg")
        axes[idx].set_ylabel("RMSSD (ms)")
        axes[idx].set_title("Heart Rate Variability")
        axes[idx].legend(fontsize=8)
        axes[idx].grid(True, alpha=0.3)

    plt.xticks(rotation=45, ha="right", fontsize=8)
    fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path


def plot_readiness_trend(readiness_df: pd.DataFrame, output_path: Path,
                         title: str = "Readiness Score Trend") -> Path:
    """Plot readiness score trend with component breakdown."""
    if readiness_df.empty or len(readiness_df) < 2:
        return _empty_plot(output_path, "Not enough readiness data")

    df = readiness_df.copy()
    dates = df["date"].astype(str)

    fig, ax = plt.subplots(figsize=(12, 5))

    score = df["score"].fillna(method="ffill")
    ax.plot(dates, score, color=COLORS["readiness"], marker="o",
            markersize=4, linewidth=1.5, label="Readiness")

    if len(score) >= 7:
        rolling = score.rolling(7).mean()
        ax.plot(dates, rolling, color=COLORS["readiness"],
                linestyle="--", linewidth=2, alpha=0.5, label="7-day avg")

    # Color zones
    ax.axhspan(85, 100, alpha=0.05, color="green")
    ax.axhspan(70, 85, alpha=0.03, color="yellow")
    ax.axhspan(0, 70, alpha=0.03, color="red")

    ax.set_ylabel("Score")
    ax.set_title(title)
    ax.set_ylim(40, 100)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path


def plot_temperature_trend(sleep_df: pd.DataFrame, output_path: Path,
                           title: str = "Temperature Deviation") -> Path:
    """Plot temperature deviation from baseline over time."""
    if sleep_df.empty or "temperature_delta" not in sleep_df.columns:
        return _empty_plot(output_path, "No temperature data available")

    df = sleep_df.dropna(subset=["temperature_delta"]).copy()
    if len(df) < 2:
        return _empty_plot(output_path, "Not enough temperature data")

    dates = df["date"].astype(str)
    temp = df["temperature_delta"]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(dates, temp, color=[COLORS["temperature"] if v > 0 else COLORS["accent"]
                                for v in temp], alpha=0.7)
    ax.axhline(0, color=COLORS["neutral"], linewidth=1)
    ax.axhline(0.5, color=COLORS["r_peaks"], linestyle="--", alpha=0.4,
               label="Elevated threshold")

    ax.set_ylabel("Temperature Delta (C)")
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right", fontsize=8)
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
