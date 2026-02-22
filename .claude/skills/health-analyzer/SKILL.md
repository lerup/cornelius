---
name: health-analyzer
description: >
  Analyze Apple Watch ECG data and Oura Ring health data. Performs ECG waveform analysis
  (R-peak detection, rhythm, HRV), sleep quality analysis, recovery trends, and cross-device
  correlation. Use when user wants to analyze health/ECG/sleep/HRV data or has placed
  health data exports in the drop folder.
---

# Health Data Analyzer

Analyze Apple Watch ECG recordings and Oura Ring health exports. Produces structured reports
with charts, HRV metrics, sleep analysis, and recovery trends.

## Setup (First Time Only)

```bash
cd ./resources/health-analyzer && bash setup.sh
```

Creates the venv and installs dependencies (~2 minutes).

## Data Preparation

User places data files in the drop folder:

```
resources/health-analyzer/data/
```

Accepted formats:
- **Apple Health export**: ZIP from iPhone Health app, OR extracted `electrocardiograms/` folder, OR individual ECG CSV files
- **Oura Ring export**: JSON from Oura web dashboard, OR CSV files (in `oura/` subfolder or with oura in filename)

## Commands

### Scan - Check what data is available

```bash
./resources/health-analyzer/run_analyze.sh scan
```

### Full Analysis

```bash
./resources/health-analyzer/run_analyze.sh run
```

### ECG Only / Oura Only

```bash
./resources/health-analyzer/run_analyze.sh run --ecg-only
./resources/health-analyzer/run_analyze.sh run --oura-only
```

### Date Filters

```bash
./resources/health-analyzer/run_analyze.sh run --date 2026-02-14
./resources/health-analyzer/run_analyze.sh run --last 7
```

### Single File Analysis

```bash
./resources/health-analyzer/run_analyze.sh ecg "/path/to/ecg_2026-02-14.csv"
./resources/health-analyzer/run_analyze.sh oura "/path/to/oura_export.json"
```

### JSON Output

```bash
./resources/health-analyzer/run_analyze.sh run --json
```

## Output

Reports are generated in:
```
resources/health-analyzer/output/YYYY-MM-DD/
├── health-report-YYYY-MM-DD.md    # Main report with findings
├── charts/                         # PNG visualizations
│   ├── ecg_waveform.png
│   ├── ecg_poincare.png
│   ├── rr_histogram.png
│   ├── hrv_metrics.png
│   ├── sleep_architecture.png
│   ├── sleep_trends.png
│   ├── hr_hrv_trends.png
│   ├── readiness_trend.png
│   ├── temperature_trend.png
│   └── hrv_comparison.png
└── metrics.json                    # Raw computed metrics
```

After analysis, open the output folder:
```bash
open ./resources/health-analyzer/output/YYYY-MM-DD
```

## Interpretation Workflow

After generating the report:

1. Read the markdown report: `resources/health-analyzer/output/YYYY-MM-DD/health-report-*.md`
2. Read metrics.json for numerical values
3. Provide interpretation to the user:
   - HRV values and autonomic balance
   - Sleep quality relative to guidelines (7-9h, 15-25% deep, 20-25% REM)
   - Recovery trajectory and actionable recommendations
   - Any rhythm irregularities that warrant medical attention
   - Cross-device correlation findings (ECG vs Oura)
4. ALWAYS include: "This analysis is informational only, not medical advice. Abnormal findings should be discussed with a physician."

## Key Metrics Reference

### HRV Benchmarks (healthy adults)
- RMSSD: 20-100ms typical (higher = better parasympathetic tone)
- SDNN: 50-150ms typical
- LF/HF ratio: ~1.0-2.0 at rest
- pNN50: 5-25% typical

### Sleep Architecture (adults)
- Deep sleep: 15-25% of total
- Light sleep: 45-55%
- REM: 20-25%
- Efficiency: >85% is good, >90% is excellent

### Oura Readiness
- 85+: Excellent recovery
- 70-84: Good
- <70: Consider lighter activity

### ECG Classifications (Apple Watch)
- sinusRhythm: Normal
- atrialFibrillation: Irregular rhythm detected - recommend physician review
- inconclusive: Signal quality issue or edge case
