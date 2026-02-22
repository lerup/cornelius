"""Sleep visualization: hypnogram, architecture, efficiency trends."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import COLORS, FIGURE_DPI, FIGURE_FORMAT


def plot_sleep_architecture(night_analysis: dict, output_path: Path,
                            title: str = None) -> Path:
    """Plot sleep architecture as stacked bar/pie for a single night."""
    arch = night_analysis.get("architecture", {})
    date_str = night_analysis.get("date", "")
    if not title:
        title = f"Sleep Architecture - {date_str}"

    stages = {
        "Deep": arch.get("deep_sleep_h", 0),
        "Light": arch.get("light_sleep_h", 0),
        "REM": arch.get("rem_sleep_h", 0),
        "Awake": arch.get("awake_h", 0),
    }

    colors = [COLORS["sleep_deep"], COLORS["sleep_light"],
              COLORS["sleep_rem"], COLORS["sleep_awake"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5),
                                    gridspec_kw={"width_ratios": [1, 1.2]})

    # Pie chart
    values = list(stages.values())
    if sum(values) > 0:
        ax1.pie(values, labels=list(stages.keys()), colors=colors,
                autopct="%1.0f%%", startangle=90, textprops={"fontsize": 10})
    ax1.set_title("Stage Distribution")

    # Bar chart with hours
    bars = ax2.bar(list(stages.keys()), list(stages.values()),
                   color=colors, edgecolor="white", width=0.6)
    for bar, val in zip(bars, values):
        if val > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                     f"{val:.1f}h", ha="center", fontsize=10)

    ax2.set_ylabel("Hours")
    ax2.set_title("Stage Duration")
    ax2.grid(True, axis="y", alpha=0.3)

    fig.suptitle(title, fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=FIGURE_DPI, format=FIGURE_FORMAT,
                bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_sleep_trends(sleep_df: pd.DataFrame, output_path: Path,
                      title: str = "Sleep Trends") -> Path:
    """Plot multi-night sleep duration and deep/REM trends."""
    if sleep_df.empty or len(sleep_df) < 2:
        return _empty_plot(output_path, "Not enough sleep data for trends")

    df = sleep_df.copy()
    for col in ["total_sleep_s", "deep_sleep_s", "rem_sleep_s"]:
        if col in df.columns:
            df[col.replace("_s", "_h")] = df[col].fillna(0) / 3600

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    dates = df["date"].astype(str)

    # Total sleep duration
    if "total_sleep_h" in df.columns:
        axes[0].bar(dates, df["total_sleep_h"], color=COLORS["ecg_signal"], alpha=0.7)
        axes[0].axhline(7, color=COLORS["neutral"], linestyle="--", alpha=0.5,
                        label="7h target")
        axes[0].set_ylabel("Hours")
        axes[0].set_title("Total Sleep Duration")
        axes[0].legend(fontsize=8)
        axes[0].grid(True, axis="y", alpha=0.3)

    # Deep + REM
    if "deep_sleep_h" in df.columns and "rem_sleep_h" in df.columns:
        axes[1].bar(dates, df["deep_sleep_h"], color=COLORS["sleep_deep"],
                    label="Deep", alpha=0.8)
        axes[1].bar(dates, df["rem_sleep_h"], bottom=df["deep_sleep_h"],
                    color=COLORS["sleep_rem"], label="REM", alpha=0.8)
        axes[1].set_ylabel("Hours")
        axes[1].set_title("Deep + REM Sleep")
        axes[1].legend(fontsize=8)
        axes[1].grid(True, axis="y", alpha=0.3)

    # Sleep score
    if "score" in df.columns:
        scores = df["score"].dropna()
        if len(scores) > 0:
            axes[2].plot(dates[:len(scores)], scores, color=COLORS["accent"],
                         marker="o", markersize=4)
            axes[2].fill_between(dates[:len(scores)], scores, alpha=0.1,
                                 color=COLORS["accent"])
            axes[2].set_ylabel("Score")
            axes[2].set_title("Sleep Score")
            axes[2].grid(True, axis="y", alpha=0.3)

    plt.xticks(rotation=45, ha="right", fontsize=8)
    fig.suptitle(title, fontsize=13)
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
