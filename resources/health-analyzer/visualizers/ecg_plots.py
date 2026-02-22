"""ECG visualization: waveform, R-peaks, Poincare, RR histogram."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from config import COLORS, FIGURE_DPI, FIGURE_FORMAT


def plot_ecg_waveform(voltage_uv: np.ndarray, r_peak_indices: np.ndarray,
                      sample_rate: int, output_path: Path,
                      window_s: tuple[float, float] = (0, 10),
                      title: str = "ECG Waveform") -> Path:
    """Plot ECG waveform with R-peak markers.

    Args:
        voltage_uv: Voltage array in microvolts
        r_peak_indices: Detected R-peak sample indices
        sample_rate: Sampling rate in Hz
        output_path: Path to save PNG
        window_s: Time window in seconds (start, end)
        title: Plot title
    """
    time_s = np.arange(len(voltage_uv)) / sample_rate
    start, end = window_s
    mask = (time_s >= start) & (time_s <= end)

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(time_s[mask], voltage_uv[mask], color=COLORS["ecg_signal"],
            linewidth=0.8, label="ECG Signal")

    # Plot R-peaks within window
    peak_mask = (r_peak_indices >= start * sample_rate) & (r_peak_indices <= end * sample_rate)
    visible_peaks = r_peak_indices[peak_mask]
    if len(visible_peaks) > 0:
        ax.scatter(visible_peaks / sample_rate, voltage_uv[visible_peaks],
                   color=COLORS["r_peaks"], s=40, zorder=5, label="R-peaks")

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Voltage (uV)")
    ax.set_title(title)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path


def plot_rr_histogram(rr_intervals_ms: np.ndarray, output_path: Path,
                      title: str = "RR Interval Distribution") -> Path:
    """Plot histogram of RR intervals."""
    if len(rr_intervals_ms) < 3:
        return _empty_plot(output_path, "Too few beats for histogram")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(rr_intervals_ms, bins=min(30, len(rr_intervals_ms) // 2 + 1),
            color=COLORS["ecg_signal"], edgecolor="white", alpha=0.8)

    mean_rr = np.mean(rr_intervals_ms)
    ax.axvline(mean_rr, color=COLORS["r_peaks"], linestyle="--", linewidth=1.5,
               label=f"Mean: {mean_rr:.0f} ms")

    ax.set_xlabel("RR Interval (ms)")
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path


def plot_poincare(rr_intervals_ms: np.ndarray, output_path: Path,
                  sd1: float = None, sd2: float = None,
                  title: str = "Poincare Plot") -> Path:
    """Plot Poincare (Lorenz) scatter: RR[n] vs RR[n+1] with SD1/SD2 ellipse."""
    if len(rr_intervals_ms) < 5:
        return _empty_plot(output_path, "Too few beats for Poincare plot")

    rr_n = rr_intervals_ms[:-1]
    rr_n1 = rr_intervals_ms[1:]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(rr_n, rr_n1, color=COLORS["ecg_signal"], s=15, alpha=0.6)

    # Identity line
    min_rr = min(rr_n.min(), rr_n1.min()) - 20
    max_rr = max(rr_n.max(), rr_n1.max()) + 20
    ax.plot([min_rr, max_rr], [min_rr, max_rr], color=COLORS["neutral"],
            linestyle="--", linewidth=0.8, alpha=0.5)

    # SD1/SD2 ellipse
    if sd1 is not None and sd2 is not None:
        from matplotlib.patches import Ellipse
        center = (np.mean(rr_n), np.mean(rr_n1))
        ellipse = Ellipse(center, width=2 * sd2, height=2 * sd1, angle=45,
                          fill=False, edgecolor=COLORS["r_peaks"], linewidth=1.5,
                          linestyle="--")
        ax.add_patch(ellipse)
        ax.annotate(f"SD1={sd1:.1f}ms", xy=(0.05, 0.95), xycoords="axes fraction",
                    fontsize=9, color=COLORS["r_peaks"])
        ax.annotate(f"SD2={sd2:.1f}ms", xy=(0.05, 0.90), xycoords="axes fraction",
                    fontsize=9, color=COLORS["r_peaks"])

    ax.set_xlabel("RR[n] (ms)")
    ax.set_ylabel("RR[n+1] (ms)")
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path


def _empty_plot(output_path: Path, message: str) -> Path:
    """Create a placeholder plot with a message."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=14,
            color=COLORS["neutral"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT)
    plt.close(fig)
    return output_path
