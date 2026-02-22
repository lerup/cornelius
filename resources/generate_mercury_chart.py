#!/usr/bin/env python3
"""
Generate Mercury Portfolio Entry Valuations scatter chart
Inflection brand identity: white background, black text, verdant green data points
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Data
data = [
    ("2021-05-05", 10.5, "Defined"),
    ("2021-09-02", 20.4, "Moonpay"),
    ("2021-09-07", 149.7, "Flashbots"),
    ("2022-02-14", 25.0, "Aptos Orbital"),
    ("2022-05-04", 70.0, "Anytype"),
    ("2022-05-09", 79.7, "Molecule"),
    ("2022-06-10", 38.6, "Hologram"),
    ("2022-12-15", 29.0, "Arx"),
    ("2022-12-15", 35.0, "Senken"),
    ("2023-01-22", 20.0, "Ora"),
    ("2023-02-10", 13.2, "Worldcoin"),
    ("2023-06-27", 55.0, "Fabric"),
    ("2023-09-11", 12.4, "Tune Insight"),
    ("2023-11-09", 17.5, "Radical Aero"),
    ("2024-07-17", 16.0, "Lodestar"),
    ("2024-09-25", 9.5, "Deep Earth"),
    ("2024-10-28", 13.8, "Ubitium"),
    ("2024-12-27", 21.5, "Ark Robotics"),
    ("2025-04-24", 25.0, "Nordic Air Defence"),
    ("2025-07-08", 9.8, "Hedy Cyber"),
    ("2025-10-07", 12.2, "Levtek Sweden AB"),
    ("2025-11-05", 17.0, "Foundational"),
]

# Parse dates and values
dates = [datetime.strptime(d[0], "%Y-%m-%d") for d in data]
valuations = [d[1] for d in data]
names = [d[2] for d in data]

# Brand colors
BACKGROUND = "#FFFFFF"
TEXT_BLACK = "#000000"
VERDANT_GREEN = "#B3BCB5"
AZURE_BLUE = "#B4BACC"
GREY = "#808080"
GRID_GREY = "#E0E0E0"

# Create figure
fig, ax = plt.subplots(figsize=(14, 8), facecolor=BACKGROUND)
ax.set_facecolor(BACKGROUND)

# Scatter plot
ax.scatter(dates, valuations, s=120, color=VERDANT_GREEN, alpha=0.85, edgecolors=VERDANT_GREEN, linewidth=1.5, zorder=3)

# Add company labels (offset slightly for readability)
for date, val, name in zip(dates, valuations, names):
    ax.annotate(
        name,
        xy=(date, val),
        xytext=(8, 0),
        textcoords="offset points",
        fontsize=8,
        color=TEXT_BLACK,
        alpha=0.7,
        va='center'
    )

# Reference lines
ax.axhline(y=29.8, color=AZURE_BLUE, linestyle='-', linewidth=2, alpha=0.7, label='Weighted Avg $29.8M', zorder=2)
ax.axhline(y=20.2, color=GREY, linestyle='-', linewidth=2, alpha=0.7, label='Median $20.2M', zorder=2)

# Styling
ax.set_xlabel('Investment Date', fontsize=11, color=TEXT_BLACK, family='sans-serif')
ax.set_ylabel('Entry Valuation ($M)', fontsize=11, color=TEXT_BLACK, family='sans-serif')
ax.set_title('mercury portfolio - entry valuations over time', fontsize=14, color=TEXT_BLACK, pad=20, family='sans-serif', loc='left')

# Grid
ax.grid(True, color=GRID_GREY, linestyle='-', linewidth=0.5, alpha=0.5, zorder=1)
ax.spines['top'].set_color(GRID_GREY)
ax.spines['right'].set_color(GRID_GREY)
ax.spines['left'].set_color(GRID_GREY)
ax.spines['bottom'].set_color(GRID_GREY)

# Date formatting on x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.xticks(rotation=45, ha='right', color=TEXT_BLACK)
plt.yticks(color=TEXT_BLACK)

# Legend
ax.legend(loc='upper left', frameon=True, facecolor=BACKGROUND, edgecolor=GRID_GREY, fontsize=9)

# Tight layout
plt.tight_layout()

# Save
output_path = '/Users/alexanderruppert/Desktop/Claude/CORNELIUS/resources/mercury-entry-valuations.png'
plt.savefig(output_path, dpi=150, facecolor=BACKGROUND, edgecolor='none', bbox_inches='tight')
print(f"Chart saved to: {output_path}")
