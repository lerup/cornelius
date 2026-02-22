import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- Inflection Brand Colors (MANDATORY) ---
COLOR_HAPS   = '#B3BCB5'   # Verdant Green - HAPS
COLOR_LEO    = '#B4BACC'   # Azure Blue - LEO
COLOR_BLACK  = '#000000'
COLOR_GRAY   = '#808080'
COLOR_WHITE  = '#FFFFFF'
COLOR_GRID   = '#D8D8D8'
COLOR_TICK   = '#B0B0B0'

# --- Data ---
# Dimensions ordered so right half = HAPS advantage, left half = LEO advantage
dimensions = [
    "Deployment\nSpeed",       # 0 - HAPS
    "Latency",                 # 1 - HAPS
    "Signal\nStrength",        # 2 - HAPS
    "Imaging\nResolution",     # 3 - HAPS
    "Dwell\nTime",             # 4 - HAPS
    "Cost\nEfficiency",        # 5 - HAPS
    "Replacement\nSpeed",      # 6 - HAPS
    "Global\nCoverage",        # 7 - LEO
    "Passive\nPersistence",    # 8 - LEO
    "Airspace\nAccess",        # 9 - LEO
    "Tech\nMaturity",          # 10 - LEO
    "Env.\nResilience",        # 11 - LEO
]

haps_scores = [92, 95, 95, 90, 95, 88, 92, 10, 15, 20, 30, 35]
leo_scores  = [12, 35, 15, 30, 10, 20, 10, 95, 90, 90, 90, 80]

N = len(dimensions)

# Angles: clockwise from top
angles = np.array([(np.pi / 2 - i * 2 * np.pi / N) % (2 * np.pi) for i in range(N)])
angles_closed = angles.tolist() + [angles[0]]
haps_closed   = haps_scores + [haps_scores[0]]
leo_closed    = leo_scores  + [leo_scores[0]]

# --- Figure ---
fig = plt.figure(figsize=(12, 9), facecolor=COLOR_WHITE)
ax = fig.add_axes([0.06, 0.09, 0.88, 0.83], polar=True, facecolor=COLOR_WHITE)
ax.spines['polar'].set_visible(False)

# --- Grid rings ---
ring_levels = [20, 40, 60, 80, 100]
for rv in ring_levels:
    circ = np.linspace(0, 2 * np.pi, 500)
    ax.plot(circ, [rv] * 500, color=COLOR_GRID, linewidth=0.7, zorder=1)

# Grid tick labels at ~3 o'clock position (angle=0 in Cartesian = rightward)
for rv in [20, 40, 60, 80]:
    ax.text(
        np.radians(6), rv + 2.5, str(rv),
        ha='left', va='bottom',
        fontsize=7, color=COLOR_TICK,
        zorder=7
    )

# Spoke lines
for a in angles:
    ax.plot([a, a], [0, 100], color=COLOR_GRID, linewidth=0.7, zorder=1)

# Dashed divider lines between HAPS and LEO zones
div1 = (angles[6] + angles[7]) / 2   # between dim 6 and 7
div2 = (angles[11] + angles[0]) / 2  # between dim 11 and 0 (top)
for d in [div1, div2]:
    ax.plot([d, d], [10, 100], color=COLOR_GRAY, linewidth=1.2,
            linestyle='--', alpha=0.35, zorder=2)

ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(0, 118)

# --- Plot HAPS ---
ax.fill(angles_closed, haps_closed, color=COLOR_HAPS, alpha=0.28, zorder=2)
ax.plot(angles_closed, haps_closed, color=COLOR_HAPS, linewidth=3, zorder=3,
        solid_joinstyle='round', solid_capstyle='round')
for a, v in zip(angles, haps_scores):
    ax.scatter(a, v, s=45, color=COLOR_HAPS, zorder=5,
               edgecolors=COLOR_WHITE, linewidth=1.5)

# --- Plot LEO ---
ax.fill(angles_closed, leo_closed, color=COLOR_LEO, alpha=0.22, zorder=2)
ax.plot(angles_closed, leo_closed, color=COLOR_LEO, linewidth=3, zorder=3,
        solid_joinstyle='round', solid_capstyle='round')
for a, v in zip(angles, leo_scores):
    ax.scatter(a, v, s=45, color=COLOR_LEO, zorder=5,
               edgecolors=COLOR_WHITE, linewidth=1.5)

# --- Zone labels inside the radar ---
# HAPS zone center: around dim 3 (lower right)
ax.text(angles[3], 58, "HAPS\nAdvantage",
        ha='center', va='center',
        fontsize=9, color=COLOR_HAPS, fontweight='bold',
        alpha=0.6, style='italic', linespacing=1.3, zorder=6)

# LEO zone center: around dim 9 (left)
ax.text(angles[9], 58, "LEO\nAdvantage",
        ha='center', va='center',
        fontsize=9, color=COLOR_LEO, fontweight='bold',
        alpha=0.6, style='italic', linespacing=1.3, zorder=6)

# --- Dimension labels ---
label_r = 113

# Per-label alignment based on angular position
label_cfg = [
    (0,  'center', 'bottom'),  # Deployment Speed - top
    (1,  'left',   'bottom'),  # Latency - upper right
    (2,  'left',   'center'),  # Signal Strength - right
    (3,  'left',   'top'),     # Imaging Resolution - lower right
    (4,  'center', 'top'),     # Dwell Time - bottom right area
    (5,  'center', 'top'),     # Cost Efficiency - bottom
    (6,  'right',  'top'),     # Replacement Speed - lower left area
    (7,  'right',  'top'),     # Global Coverage - lower left
    (8,  'right',  'center'),  # Passive Persistence - left
    (9,  'right',  'bottom'),  # Airspace Access - upper left
    (10, 'right',  'bottom'),  # Tech Maturity - upper left
    (11, 'center', 'bottom'),  # Env. Resilience - top left
]

for idx, ha, va in label_cfg:
    a = angles[idx]
    # Color label by which series wins
    lc = COLOR_HAPS if haps_scores[idx] > leo_scores[idx] else COLOR_LEO
    ax.text(a, label_r, dimensions[idx],
            ha=ha, va=va,
            fontsize=10, fontweight='600',
            color=lc, linespacing=1.25,
            multialignment='center',
            zorder=8)

# --- Title ---
fig.text(0.5, 0.985,
         "HAPS vs LEO Satellite: Capability Comparison",
         ha='center', va='top',
         fontsize=17, fontweight='bold',
         color=COLOR_BLACK)

fig.text(0.5, 0.948,
         "12-axis analysis  \u00b7  Deployment, signal performance, coverage, and operational resilience",
         ha='center', va='top',
         fontsize=10, color=COLOR_GRAY)

# --- Legend ---
patch_haps = mpatches.Patch(
    facecolor=COLOR_HAPS, edgecolor=COLOR_HAPS, alpha=0.75,
    label='HAPS (Stratospheric)'
)
patch_leo = mpatches.Patch(
    facecolor=COLOR_LEO, edgecolor=COLOR_LEO, alpha=0.75,
    label='LEO Satellite'
)
legend = fig.legend(
    handles=[patch_haps, patch_leo],
    loc='lower center',
    bbox_to_anchor=(0.5, 0.005),
    ncol=2,
    frameon=False,
    fontsize=11,
    handlelength=1.6,
    handleheight=0.9,
    columnspacing=3.0
)
for t in legend.get_texts():
    t.set_color(COLOR_BLACK)
    t.set_fontweight('600')

# --- Source line ---
fig.text(
    0.025, 0.012,
    "Source: HAPS Alliance Whitepaper, Apr 2025; FSPL calculations at 10 GHz",
    ha='left', va='bottom',
    fontsize=7.5, color=COLOR_GRAY,
    style='italic'
)

# --- Save raw chart (no logo yet) ---
out_raw = "/Users/alexanderruppert/Desktop/Claude/OBSIDIAN VAULT/04-Output/Articles/when-leo-fails/images/haps-vs-leo-raw.png"
plt.savefig(
    out_raw,
    dpi=150,
    bbox_inches='tight',
    facecolor=COLOR_WHITE,
    edgecolor='none'
)
print(f"Saved raw: {out_raw}")
plt.close()
