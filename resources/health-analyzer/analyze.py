#!/usr/bin/env python3
"""Health Data Analyzer - Main CLI.

Usage:
    python analyze.py scan                           # Scan data/ folder
    python analyze.py run                            # Full analysis pipeline
    python analyze.py run --ecg-only                 # ECG analysis only
    python analyze.py run --oura-only                # Oura analysis only
    python analyze.py run --date 2026-02-14          # Specific date
    python analyze.py run --last 7                   # Last N days
    python analyze.py ecg /path/to/ecg.csv           # Single ECG file
    python analyze.py oura /path/to/oura.json        # Oura data only
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Ensure project root is on path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_DIR, OUTPUT_DIR, RPEAK_DETECTOR, HRV_MIN_BEATS


def cmd_scan(args):
    """Scan data folder and report what's available."""
    from parsers.apple_ecg import find_ecg_data
    from parsers.oura import find_oura_data

    print("Scanning data folder:", DATA_DIR)
    print("=" * 60)

    # ECG data
    ecg_files = find_ecg_data(DATA_DIR)
    if ecg_files:
        dates = [str(e["date"].date()) if e["date"] else "unknown" for e in ecg_files]
        classifications = [e["classification"] for e in ecg_files]
        print(f"\nApple Watch ECG: {len(ecg_files)} recording(s)")
        print(f"  Date range: {dates[0]} to {dates[-1]}")
        print(f"  Classifications: {', '.join(set(classifications))}")
        for e in ecg_files:
            d = str(e["date"].date()) if e["date"] else "?"
            print(f"    {d} - {e['classification']} - {e['num_samples']} samples - {Path(e['filepath']).name}")
    else:
        print("\nApple Watch ECG: No data found")
        print("  Place ECG CSV files or Apple Health export.zip in:", DATA_DIR)

    # Oura data
    oura = find_oura_data(DATA_DIR)
    if oura:
        dr = oura["date_range"]
        print(f"\nOura Ring: {oura['num_nights']} night(s)")
        print(f"  Date range: {dr[0]} to {dr[1]}")
        for key in ["sleep", "readiness", "activity"]:
            df = oura[key]
            if not df.empty:
                print(f"  {key.title()}: {len(df)} records")
    else:
        print("\nOura Ring: No data found")
        print("  Place Oura JSON export or CSV files in:", DATA_DIR)

    print("\n" + "=" * 60)
    if ecg_files or oura:
        print("Ready for analysis. Run: ./run_analyze.sh run")
    else:
        print("No data found. Place health data exports in:", DATA_DIR)


def cmd_run(args):
    """Run full analysis pipeline."""
    import numpy as np
    from parsers.apple_ecg import find_ecg_data
    from parsers.oura import find_oura_data
    from analyzers.ecg_analysis import analyze_ecg_recording
    from analyzers.hrv_analysis import (compute_hrv_from_rr, contextualize_hrv,
                                         compute_hrv_from_oura, compare_hrv_sources)
    from analyzers.sleep_analysis import analyze_sleep_night, analyze_sleep_trends
    from analyzers.recovery_analysis import (analyze_readiness, analyze_temperature,
                                              compute_recovery_trajectory)
    from analyzers.cross_correlation import correlate_ecg_oura
    from report import generate_report

    # Create output directory
    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(args.output_dir) if args.output_dir else OUTPUT_DIR / today
    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    ecg_results = None
    oura_data = None
    sleep_trends_result = None
    readiness_result = None
    temperature_result = None
    recovery_result = None
    cross_result = None
    hrv_context = None
    chart_paths = []

    detector = args.detector if hasattr(args, "detector") and args.detector else RPEAK_DETECTOR

    # --- ECG Analysis ---
    if not args.oura_only:
        print("Loading ECG data...")
        ecg_files = find_ecg_data(DATA_DIR)

        if args.date:
            target = datetime.strptime(args.date, "%Y-%m-%d").date()
            ecg_files = [e for e in ecg_files
                         if e["date"] and e["date"].date() == target]
        elif args.last:
            cutoff = date.today() - timedelta(days=args.last)
            ecg_files = [e for e in ecg_files
                         if e["date"] and e["date"].date() >= cutoff]

        if ecg_files:
            print(f"Analyzing {len(ecg_files)} ECG recording(s)...")
            ecg_results = []
            for ecg_data in ecg_files:
                analysis = analyze_ecg_recording(ecg_data, method=detector)
                ecg_results.append(analysis)

                # HRV from ECG
                rr = analysis.get("r_peaks", {}).get("rr_intervals_ms", [])
                if len(rr) >= HRV_MIN_BEATS:
                    hrv = compute_hrv_from_rr(np.array(rr))
                    analysis["hrv"] = hrv
                    hrv_context = contextualize_hrv(hrv)

            # Generate ECG charts (for first recording with good quality)
            good_ecg = [r for r in ecg_results
                        if r.get("signal_quality", {}).get("quality_label") != "poor"
                        and len(r.get("r_peak_indices", [])) > 0]

            if good_ecg:
                from visualizers.ecg_plots import (plot_ecg_waveform, plot_rr_histogram,
                                                    plot_poincare)
                r = good_ecg[0]
                voltage = r["voltage_uv"]
                peaks = r["r_peak_indices"]
                sr = r["recording"]["sample_rate"]
                rr = np.array(r["r_peaks"]["rr_intervals_ms"])

                p = plot_ecg_waveform(voltage, peaks, sr,
                                       charts_dir / "ecg_waveform.png")
                chart_paths.append(p)

                if len(rr) >= 3:
                    p = plot_rr_histogram(rr, charts_dir / "rr_histogram.png")
                    chart_paths.append(p)

                if len(rr) >= 5:
                    sd1 = r.get("hrv", {}).get("nonlinear", {}).get("SD1_ms")
                    sd2 = r.get("hrv", {}).get("nonlinear", {}).get("SD2_ms")
                    p = plot_poincare(rr, charts_dir / "ecg_poincare.png",
                                      sd1=sd1, sd2=sd2)
                    chart_paths.append(p)

            # HRV summary chart
            if ecg_results and ecg_results[0].get("hrv"):
                from visualizers.hrv_plots import plot_hrv_summary
                p = plot_hrv_summary(ecg_results[0]["hrv"],
                                      charts_dir / "hrv_metrics.png")
                chart_paths.append(p)

            print(f"  ECG analysis complete: {len(ecg_results)} recording(s)")
        else:
            print("  No ECG data found")

    # --- Oura Analysis ---
    if not args.ecg_only:
        print("Loading Oura data...")
        oura_data = find_oura_data(DATA_DIR)

        if oura_data:
            sleep_df = oura_data["sleep"]
            readiness_df = oura_data["readiness"]

            if args.date:
                target = datetime.strptime(args.date, "%Y-%m-%d").date()
                if not sleep_df.empty:
                    sleep_df = sleep_df[sleep_df["date"] == target]
                if not readiness_df.empty:
                    readiness_df = readiness_df[readiness_df["date"] == target]
            elif args.last:
                cutoff = date.today() - timedelta(days=args.last)
                if not sleep_df.empty:
                    sleep_df = sleep_df[sleep_df["date"] >= cutoff]
                if not readiness_df.empty:
                    readiness_df = readiness_df[readiness_df["date"] >= cutoff]

            # Sleep analysis
            if not sleep_df.empty:
                from analyzers.sleep_analysis import analyze_sleep_night, analyze_sleep_trends
                latest_night = analyze_sleep_night(sleep_df.iloc[-1])
                sleep_trends_result = analyze_sleep_trends(sleep_df)

                # Sleep charts
                from visualizers.sleep_plots import (plot_sleep_architecture,
                                                      plot_sleep_trends)
                p = plot_sleep_architecture(latest_night,
                                             charts_dir / "sleep_architecture.png")
                chart_paths.append(p)

                if len(sleep_df) >= 2:
                    p = plot_sleep_trends(sleep_df, charts_dir / "sleep_trends.png")
                    chart_paths.append(p)

                # HR/HRV trends
                from visualizers.trends_plots import plot_hr_hrv_trends, plot_temperature_trend
                if len(sleep_df) >= 2:
                    p = plot_hr_hrv_trends(sleep_df, charts_dir / "hr_hrv_trends.png")
                    chart_paths.append(p)

                # Temperature
                temperature_result = analyze_temperature(sleep_df)
                if not temperature_result.get("error"):
                    p = plot_temperature_trend(sleep_df,
                                                charts_dir / "temperature_trend.png")
                    chart_paths.append(p)

                print(f"  Sleep analysis: {len(sleep_df)} night(s)")

            # Readiness analysis
            if not readiness_df.empty:
                readiness_result = analyze_readiness(readiness_df)

                from visualizers.trends_plots import plot_readiness_trend
                if len(readiness_df) >= 2:
                    p = plot_readiness_trend(readiness_df,
                                              charts_dir / "readiness_trend.png")
                    chart_paths.append(p)

                print(f"  Readiness analysis: {len(readiness_df)} day(s)")

            # Recovery trajectory
            recovery_result = compute_recovery_trajectory(readiness_df, sleep_df)
        else:
            print("  No Oura data found")

    # --- Cross-Correlation ---
    if ecg_results and oura_data:
        print("Computing cross-device correlation...")
        cross_result = correlate_ecg_oura(ecg_results, oura_data)

        # HRV comparison chart
        hrv_corr = cross_result.get("hrv_correlation")
        if hrv_corr:
            from visualizers.hrv_plots import plot_hrv_comparison
            matched = cross_result.get("matched_days", [])
            dates = [d["date"] for d in matched if "ecg_rmssd_ms" in d]
            ecg_vals = hrv_corr.get("ecg_rmssd_values", [])
            oura_vals = hrv_corr.get("oura_rmssd_values", [])
            if ecg_vals and oura_vals:
                p = plot_hrv_comparison(ecg_vals, oura_vals, dates,
                                         charts_dir / "hrv_comparison.png")
                chart_paths.append(p)

    # --- Generate Report ---
    print("Generating report...")

    # Clean ecg_results for report (remove large arrays)
    ecg_for_report = None
    if ecg_results:
        ecg_for_report = []
        for r in ecg_results:
            clean = {k: v for k, v in r.items()
                     if k not in ("voltage_uv", "r_peak_indices")}
            ecg_for_report.append(clean)

    report_path = generate_report(
        ecg_results=ecg_for_report,
        oura_results=oura_data,
        sleep_trends=sleep_trends_result,
        readiness_results=readiness_result,
        temperature_results=temperature_result,
        recovery_trajectory=recovery_result,
        cross_results=cross_result,
        hrv_context=hrv_context,
        charts=chart_paths,
        output_dir=out_dir,
    )

    print(f"\nReport saved to: {report_path}")
    print(f"Charts saved to: {charts_dir}")
    print(f"Metrics saved to: {out_dir / 'metrics.json'}")

    if args.json:
        metrics_path = out_dir / "metrics.json"
        print("\n--- JSON OUTPUT ---")
        print(metrics_path.read_text())

    return report_path


def cmd_ecg(args):
    """Analyze a single ECG file."""
    import numpy as np
    from parsers.apple_ecg import parse_ecg_csv
    from analyzers.ecg_analysis import analyze_ecg_recording
    from analyzers.hrv_analysis import compute_hrv_from_rr, contextualize_hrv

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Analyzing ECG file: {filepath}")
    ecg_data = parse_ecg_csv(filepath)
    result = analyze_ecg_recording(ecg_data)

    # HRV
    rr = result.get("r_peaks", {}).get("rr_intervals_ms", [])
    if len(rr) >= HRV_MIN_BEATS:
        hrv = compute_hrv_from_rr(np.array(rr))
        result["hrv"] = hrv
        result["hrv_context"] = contextualize_hrv(hrv)

    # Output
    output = {k: v for k, v in result.items()
              if k not in ("voltage_uv", "r_peak_indices")}

    if args.json:
        print(json.dumps(output, indent=2, default=str))
    else:
        _print_ecg_summary(result)


def cmd_oura(args):
    """Analyze Oura data."""
    from parsers.oura import parse_oura_auto
    from analyzers.sleep_analysis import analyze_sleep_night, analyze_sleep_trends
    from analyzers.recovery_analysis import analyze_readiness, analyze_temperature

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Analyzing Oura data: {filepath}")
    oura_data = parse_oura_auto(filepath)

    sleep_df = oura_data["sleep"]
    if not sleep_df.empty:
        latest = analyze_sleep_night(sleep_df.iloc[-1])
        trends = analyze_sleep_trends(sleep_df)

        if args.json:
            print(json.dumps({"latest_night": latest, "trends": trends},
                             indent=2, default=str))
        else:
            _print_oura_summary(latest, trends)


def _print_ecg_summary(result):
    rec = result.get("recording", {})
    quality = result.get("signal_quality", {})
    peaks = result.get("r_peaks", {})
    rhythm = result.get("rhythm", {})

    print(f"\n{'='*50}")
    print(f"Date: {rec.get('date', 'unknown')}")
    print(f"Classification: {rec.get('classification', 'N/A')}")
    print(f"Duration: {rec.get('duration_s', 'N/A')} s")
    print(f"Signal Quality: {quality.get('quality_label', 'N/A')} ({quality.get('quality_score', 'N/A')})")
    print(f"Beats Detected: {peaks.get('num_beats', 0)}")
    print(f"Mean HR: {peaks.get('mean_hr_bpm', 'N/A')} bpm")
    print(f"Rhythm Regular: {rhythm.get('rhythm_regular', 'N/A')}")

    hrv = result.get("hrv", {})
    td = hrv.get("time_domain", {})
    if td and "error" not in td:
        print(f"\nHRV Metrics:")
        print(f"  RMSSD: {td.get('RMSSD_ms', 'N/A')} ms")
        print(f"  SDNN: {td.get('SDNN_ms', 'N/A')} ms")
        print(f"  pNN50: {td.get('pNN50_pct', 'N/A')}%")
        print(f"  Mean HR: {td.get('MeanHR_bpm', 'N/A')} bpm")

    ctx = result.get("hrv_context", {})
    if ctx:
        print(f"\nInterpretation:")
        for k, v in ctx.items():
            print(f"  {k}: {v}")

    print(f"{'='*50}")


def _print_oura_summary(latest_night, trends):
    arch = latest_night.get("architecture", {})
    qual = latest_night.get("quality", {})

    print(f"\n{'='*50}")
    print(f"Latest Night: {latest_night.get('date', 'unknown')}")
    print(f"Total Sleep: {arch.get('total_sleep_h', 'N/A')} h")
    print(f"  Deep: {arch.get('deep_sleep_h', 'N/A')} h ({arch.get('deep_pct', 'N/A')}%)")
    print(f"  Light: {arch.get('light_sleep_h', 'N/A')} h ({arch.get('light_pct', 'N/A')}%)")
    print(f"  REM: {arch.get('rem_sleep_h', 'N/A')} h ({arch.get('rem_pct', 'N/A')}%)")
    print(f"Efficiency: {qual.get('efficiency_pct', 'N/A')}%")
    print(f"Score: {qual.get('score', 'N/A')}")

    if trends and "duration" in trends:
        dur = trends["duration"]
        print(f"\nTrends ({trends.get('num_nights', 'N/A')} nights):")
        print(f"  Avg Duration: {dur.get('mean_h', 'N/A')} h")
        if "trend_direction" in dur:
            print(f"  Duration Trend: {dur['trend_direction']}")

    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(
        description="Health Data Analyzer - Apple Watch ECG + Oura Ring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scan                        Scan data folder
  %(prog)s run                         Full analysis
  %(prog)s run --ecg-only              ECG only
  %(prog)s run --oura-only             Oura only
  %(prog)s run --last 7                Last 7 days
  %(prog)s ecg /path/to/ecg.csv        Single ECG file
  %(prog)s oura /path/to/oura.json     Oura export
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # scan
    scan_parser = subparsers.add_parser("scan", help="Scan data folder")

    # run
    run_parser = subparsers.add_parser("run", help="Run full analysis")
    run_parser.add_argument("--ecg-only", action="store_true",
                            help="Only analyze ECG data")
    run_parser.add_argument("--oura-only", action="store_true",
                            help="Only analyze Oura data")
    run_parser.add_argument("--date", type=str,
                            help="Analyze specific date (YYYY-MM-DD)")
    run_parser.add_argument("--last", type=int,
                            help="Analyze last N days")
    run_parser.add_argument("--detector", type=str, default=RPEAK_DETECTOR,
                            help=f"R-peak detector method (default: {RPEAK_DETECTOR})")
    run_parser.add_argument("--output-dir", type=str,
                            help="Output directory")
    run_parser.add_argument("--json", action="store_true",
                            help="Output metrics as JSON")

    # ecg
    ecg_parser = subparsers.add_parser("ecg", help="Analyze single ECG file")
    ecg_parser.add_argument("file", type=str, help="Path to ECG CSV file")
    ecg_parser.add_argument("--detector", type=str, default=RPEAK_DETECTOR)
    ecg_parser.add_argument("--json", action="store_true")

    # oura
    oura_parser = subparsers.add_parser("oura", help="Analyze Oura data")
    oura_parser.add_argument("file", type=str, help="Path to Oura JSON/CSV")
    oura_parser.add_argument("--last", type=int)
    oura_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "ecg":
        cmd_ecg(args)
    elif args.command == "oura":
        cmd_oura(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
