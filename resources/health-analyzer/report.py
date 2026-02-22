"""Markdown report generator for health analysis results."""
import json
from datetime import datetime
from pathlib import Path

from config import MEDICAL_DISCLAIMER, REPORT_PREFIX


def generate_report(ecg_results: list[dict] | None,
                    oura_results: dict | None,
                    sleep_trends: dict | None,
                    readiness_results: dict | None,
                    temperature_results: dict | None,
                    recovery_trajectory: dict | None,
                    cross_results: dict | None,
                    hrv_context: dict | None,
                    charts: list[Path] | None,
                    output_dir: Path) -> Path:
    """Generate comprehensive health analysis report.

    Returns: Path to generated markdown report.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    report_name = f"{REPORT_PREFIX}-{now.strftime('%Y-%m-%d')}.md"
    report_path = output_dir / report_name

    sections = []

    # Header
    sections.append(f"# Health Data Analysis Report")
    sections.append(f"> Generated: {now.strftime('%Y-%m-%d %H:%M')}")
    sections.append(f"> {MEDICAL_DISCLAIMER}")
    sections.append("")

    # Summary
    sections.append("## Summary")
    sections.append("")
    summary_points = _build_summary(ecg_results, oura_results, sleep_trends,
                                     readiness_results, recovery_trajectory)
    for point in summary_points:
        sections.append(f"- {point}")
    sections.append("")

    # ECG Section
    if ecg_results:
        sections.extend(_ecg_section(ecg_results, hrv_context))

    # Sleep Section
    if oura_results:
        sections.extend(_sleep_section(oura_results, sleep_trends))

    # Recovery Section
    if readiness_results or temperature_results:
        sections.extend(_recovery_section(readiness_results, temperature_results,
                                           recovery_trajectory))

    # Cross-Correlation Section
    if cross_results and "error" not in cross_results:
        sections.extend(_cross_correlation_section(cross_results))

    # Charts reference
    if charts:
        sections.append("## Charts")
        sections.append("")
        for chart_path in charts:
            rel = chart_path.name if isinstance(chart_path, Path) else str(chart_path)
            name = rel.replace(".png", "").replace("_", " ").title()
            sections.append(f"![{name}](charts/{rel})")
            sections.append("")

    # Raw metrics
    sections.append("## Raw Metrics")
    sections.append("")
    metrics = _collect_metrics(ecg_results, oura_results, sleep_trends,
                                readiness_results, cross_results)
    sections.append("```json")
    sections.append(json.dumps(metrics, indent=2, default=str))
    sections.append("```")

    report_content = "\n".join(sections)
    report_path.write_text(report_content, encoding="utf-8")

    # Also save metrics.json
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")

    return report_path


def _build_summary(ecg_results, oura_results, sleep_trends,
                    readiness_results, recovery_trajectory):
    points = []

    if ecg_results:
        n = len(ecg_results)
        classifications = set()
        for r in ecg_results:
            cls = r.get("recording", {}).get("classification", "")
            if cls:
                classifications.add(cls)
        points.append(f"{n} ECG recording(s) analyzed - classifications: {', '.join(classifications)}")

        # Average HR across recordings
        hrs = [r.get("r_peaks", {}).get("mean_hr_bpm") for r in ecg_results
               if r.get("r_peaks", {}).get("mean_hr_bpm")]
        if hrs:
            points.append(f"Average heart rate across ECG recordings: {sum(hrs)/len(hrs):.0f} bpm")

    if oura_results:
        sleep_df = oura_results.get("sleep")
        if sleep_df is not None and not sleep_df.empty:
            points.append(f"{len(sleep_df)} nights of Oura sleep data analyzed")

    if sleep_trends and "duration" in sleep_trends:
        avg = sleep_trends["duration"].get("mean_h")
        if avg:
            points.append(f"Average sleep duration: {avg:.1f} hours")

    if readiness_results and "score" in readiness_results:
        latest = readiness_results["score"].get("latest")
        cat = readiness_results["score"].get("category", "")
        if latest:
            points.append(f"Latest readiness score: {latest} ({cat})")

    if recovery_trajectory:
        traj = recovery_trajectory.get("trajectory", "")
        if traj and traj != "insufficient_data":
            points.append(f"Recovery trajectory: {traj}")

    if not points:
        points.append("No health data found. Place files in the data/ folder.")

    return points


def _ecg_section(ecg_results, hrv_context):
    lines = ["## ECG Analysis", ""]

    for i, result in enumerate(ecg_results):
        rec = result.get("recording", {})
        quality = result.get("signal_quality", {})
        peaks = result.get("r_peaks", {})
        rhythm = result.get("rhythm", {})

        date_str = rec.get("date", "unknown")
        lines.append(f"### Recording {i+1} - {date_str}")
        lines.append("")

        # Metadata table
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        lines.append(f"| Classification | {rec.get('classification', 'N/A')} |")
        lines.append(f"| Duration | {rec.get('duration_s', 'N/A')} s |")
        lines.append(f"| Sample Rate | {rec.get('sample_rate', 'N/A')} Hz |")
        lines.append(f"| Signal Quality | {quality.get('quality_label', 'N/A')} ({quality.get('quality_score', 'N/A')}) |")
        lines.append(f"| Beats Detected | {peaks.get('num_beats', 'N/A')} |")
        lines.append(f"| Mean HR (detected) | {peaks.get('mean_hr_bpm', 'N/A')} bpm |")
        lines.append(f"| Mean HR (reported) | {rec.get('average_hr_reported', 'N/A')} bpm |")
        lines.append(f"| Rhythm Regular | {rhythm.get('rhythm_regular', 'N/A')} |")
        lines.append(f"| CV of RR | {rhythm.get('cv_rr', 'N/A')} |")
        lines.append(f"| Premature Beats | {rhythm.get('premature_beats', 'N/A')} |")
        lines.append(f"| Detection Method | {peaks.get('method', 'N/A')} |")
        lines.append("")

    # HRV context
    if hrv_context:
        lines.append("### HRV Interpretation")
        lines.append("")
        for metric, interpretation in hrv_context.items():
            lines.append(f"- **{metric.upper()}**: {interpretation}")
        lines.append("")

    return lines


def _sleep_section(oura_results, sleep_trends):
    lines = ["## Sleep Analysis", ""]

    sleep_df = oura_results.get("sleep")
    if sleep_df is not None and not sleep_df.empty:
        # Latest night
        latest = sleep_df.iloc[-1].to_dict()
        lines.append("### Latest Night")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|---|---|")

        total_h = (latest.get("total_sleep_s", 0) or 0) / 3600
        lines.append(f"| Total Sleep | {total_h:.1f} h |")
        lines.append(f"| Deep Sleep | {(latest.get('deep_sleep_s', 0) or 0) / 3600:.1f} h |")
        lines.append(f"| REM Sleep | {(latest.get('rem_sleep_s', 0) or 0) / 3600:.1f} h |")
        lines.append(f"| Efficiency | {latest.get('efficiency', 'N/A')}% |")
        lines.append(f"| Sleep Score | {latest.get('score', 'N/A')} |")
        lines.append(f"| Lowest HR | {latest.get('lowest_hr', 'N/A')} bpm |")
        lines.append(f"| Average HRV | {latest.get('average_hrv', 'N/A')} ms |")
        lines.append(f"| Temperature Delta | {latest.get('temperature_delta', 'N/A')} C |")
        lines.append("")

    # Trends
    if sleep_trends and "duration" in sleep_trends:
        lines.append("### Sleep Trends")
        lines.append("")
        dur = sleep_trends["duration"]
        lines.append(f"- Average duration: {dur.get('mean_h', 'N/A')} h (std: {dur.get('std_h', 'N/A')} h)")
        if "trend_direction" in dur:
            lines.append(f"- Duration trend: {dur['trend_direction']}")

        if "hrv_trend" in sleep_trends:
            hrv = sleep_trends["hrv_trend"]
            lines.append(f"- HRV mean: {hrv.get('mean_ms', 'N/A')} ms (range: {hrv.get('min_ms', 'N/A')}-{hrv.get('max_ms', 'N/A')} ms)")
            if "trend_direction" in hrv:
                lines.append(f"- HRV trend: {hrv['trend_direction']}")

        if "resting_hr_trend" in sleep_trends:
            hr = sleep_trends["resting_hr_trend"]
            lines.append(f"- Resting HR mean: {hr.get('mean_bpm', 'N/A')} bpm")
            if "trend_direction" in hr:
                lines.append(f"- Resting HR trend: {hr['trend_direction']}")

        lines.append("")

    return lines


def _recovery_section(readiness_results, temperature_results, recovery_trajectory):
    lines = ["## Recovery & Readiness", ""]

    if readiness_results and "score" in readiness_results:
        score_data = readiness_results["score"]
        lines.append("### Readiness Score")
        lines.append("")
        lines.append(f"- Latest: **{score_data.get('latest', 'N/A')}** ({score_data.get('category', '')})")
        lines.append(f"- Average: {score_data.get('mean', 'N/A')} (range: {score_data.get('min', 'N/A')}-{score_data.get('max', 'N/A')})")
        if "trend_7d" in score_data:
            lines.append(f"- 7-day trend: {score_data['trend_7d']}")
        lines.append("")

        # Weakest components
        weakest = readiness_results.get("weakest", [])
        if weakest:
            lines.append("**Areas needing attention:**")
            for w in weakest:
                lines.append(f"- {w['component']}: {w['score']}")
            lines.append("")

    if temperature_results and "error" not in temperature_results:
        lines.append("### Temperature")
        lines.append("")
        lines.append(f"- Latest delta: {temperature_results.get('latest_delta', 'N/A')} C")
        lines.append(f"- Mean delta: {temperature_results.get('mean_delta', 'N/A')} C")
        if temperature_results.get("elevated_flag"):
            n = len(temperature_results.get("elevated_days", []))
            lines.append(f"- **{n} elevated day(s) detected** (delta > 0.5 C)")
        lines.append("")

    if recovery_trajectory and recovery_trajectory.get("trajectory") != "insufficient_data":
        lines.append("### Recovery Trajectory")
        lines.append("")
        lines.append(f"- Overall: **{recovery_trajectory['trajectory']}**")
        for signal, direction in recovery_trajectory.get("signals", {}).items():
            lines.append(f"- {signal}: {direction}")
        lines.append("")

    return lines


def _cross_correlation_section(cross_results):
    lines = ["## Cross-Device Correlation (ECG + Oura)", ""]

    lines.append(f"- Matched days: {cross_results.get('num_matched', 0)}")
    lines.append("")

    # HRV comparison
    hrv_corr = cross_results.get("hrv_correlation")
    if hrv_corr:
        lines.append("### HRV: ECG vs Oura")
        lines.append("")
        lines.append(f"- ECG RMSSD mean: {hrv_corr.get('mean_ecg_rmssd', 'N/A')} ms")
        lines.append(f"- Oura RMSSD mean: {hrv_corr.get('mean_oura_rmssd', 'N/A')} ms")
        lines.append(f"- Mean difference: {hrv_corr.get('mean_difference_ms', 'N/A')} ms")
        lines.append(f"- Correlation (Pearson r): {hrv_corr.get('pearson_r', 'N/A')}")
        lines.append(f"- Note: {hrv_corr.get('note', '')}")
        lines.append("")

    # Flags
    flags = cross_results.get("flags", [])
    if flags:
        lines.append("### Flags")
        lines.append("")
        for flag in flags:
            lines.append(f"- {flag}")
        lines.append("")

    return lines


def _collect_metrics(ecg_results, oura_results, sleep_trends,
                      readiness_results, cross_results):
    """Collect all metrics into a JSON-serializable dict."""
    metrics = {}

    if ecg_results:
        metrics["ecg"] = []
        for r in ecg_results:
            entry = {
                "date": r.get("recording", {}).get("date"),
                "classification": r.get("recording", {}).get("classification"),
                "signal_quality": r.get("signal_quality"),
                "num_beats": r.get("r_peaks", {}).get("num_beats"),
                "mean_hr_bpm": r.get("r_peaks", {}).get("mean_hr_bpm"),
                "rhythm": r.get("rhythm"),
            }
            metrics["ecg"].append(entry)

    if sleep_trends:
        metrics["sleep_trends"] = {k: v for k, v in sleep_trends.items()
                                    if k != "error"}

    if readiness_results:
        metrics["readiness"] = {k: v for k, v in readiness_results.items()
                                 if k != "error"}

    if cross_results:
        metrics["cross_correlation"] = {
            k: v for k, v in cross_results.items()
            if k not in ("error", "matched_days")  # matched_days can be large
        }

    return metrics
