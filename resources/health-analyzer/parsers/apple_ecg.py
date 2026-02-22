"""Apple Watch ECG CSV parser.

Apple Health exports ECG recordings as CSV files in an electrocardiograms/ directory.
Each file is a 30-second, single-lead (Lead I) recording at 512 Hz.

CSV structure:
- ~13 metadata rows as key,value pairs (Name, Recording Date, Classification, etc.)
- Blank row separator
- Single column of voltage measurements in microvolts
"""
import csv
import zipfile
from datetime import datetime
from pathlib import Path

import numpy as np


def _parse_metadata_rows(rows: list[list[str]]) -> dict:
    """Extract metadata from the header rows of an Apple Watch ECG CSV.

    Handles localized field names (English, German, etc.) by normalizing
    to canonical English keys.
    """
    # Map localized field names to canonical English keys
    FIELD_MAP = {
        # German
        "name": "name",
        "geburtstag": "birthday",
        "aufzeichnungsdatum": "recording_date",
        "klassifizierung": "classification",
        "symptome": "symptoms",
        "softwareversion": "software_version",
        "gerät": "device",
        "messrate": "sample_rate",
        "ableitung": "lead",
        "einheit": "unit",
        "durchschnittliche_herzfrequenz": "average_heart_rate",
        # English
        "recording_date": "recording_date",
        "classification": "classification",
        "device": "device",
        "sample_rate": "sample_rate",
        "sampling_frequency_(hz)": "sample_rate",
        "average_heart_rate": "average_heart_rate",
        "software_version": "software_version",
        "lead": "lead",
        "unit": "unit",
        "source": "device",
    }

    meta = {}
    for row in rows:
        if len(row) >= 2:
            raw_key = row[0].strip().lower().replace(" ", "_")
            val = row[1].strip()
            canonical = FIELD_MAP.get(raw_key, raw_key)
            meta[canonical] = val
    return meta


def _extract_classification(meta: dict) -> str:
    """Normalize the ECG classification string.

    Handles English and German classification values from Apple Health.
    """
    raw = meta.get("classification", "unknown")
    mapping = {
        # English
        "sinusrhythm": "sinusRhythm",
        "sinusrhythmus": "sinusRhythm",
        "atrialfibrillation": "atrialFibrillation",
        "vorhofflimmern": "atrialFibrillation",
        "inconclusivelowheartratenotification": "inconclusiveLowHR",
        "inconclusivehighheartratenotification": "inconclusiveHighHR",
        "inconclusive": "inconclusive",
        "uneindeutig": "inconclusive",
        # German
        "schlechteaufzeichnung": "poorRecording",
        "schlechteaufnahme": "poorRecording",
        "poorrecording": "poorRecording",
        "hoheherfrequenz": "inconclusiveHighHR",
        "niedrigeherzfrequenz": "inconclusiveLowHR",
    }
    normalized = raw.lower().replace(" ", "").replace("_", "").replace("-", "")
    return mapping.get(normalized, raw)


def _parse_date(meta: dict) -> datetime | None:
    """Try to parse the recording date from metadata.

    Handles formats like:
    - "2026-02-14 03:39:24 +0100"
    - "2026-02-14 03:39:24"
    - "2026-02-14T03:39:24+01:00"
    - "2026-02-14"
    """
    raw = meta.get("recording_date", meta.get("date", ""))
    if not raw:
        return None
    formats = [
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    # Fallback: try extracting just the date portion
    try:
        date_part = raw[:10]
        return datetime.strptime(date_part, "%Y-%m-%d")
    except (ValueError, IndexError):
        return None


def parse_ecg_csv(filepath: Path) -> dict:
    """Parse a single Apple Watch ECG CSV file.

    Returns dict with keys:
        date, classification, average_hr, device, sample_rate,
        voltage_uv (np.ndarray), duration_s, num_samples, filepath
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"ECG file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        all_rows = list(reader)

    # Split metadata from voltage data
    # Apple Health CSV has: metadata rows, blank line, lead/unit rows, blank line, voltages
    # Collect all non-voltage rows as metadata, then find where numbers start
    meta_rows = []
    voltage_start = 0
    found_first_blank = False

    for i, row in enumerate(all_rows):
        is_blank = not row or (len(row) == 1 and row[0].strip() == "")

        if is_blank:
            found_first_blank = True
            continue

        # Check if this row is a single numeric value (voltage data)
        if len(row) == 1 and found_first_blank:
            try:
                float(row[0])
                voltage_start = i
                break
            except ValueError:
                pass

        # Still in metadata/header territory
        meta_rows.append(row)

    meta = _parse_metadata_rows(meta_rows)

    # Parse voltage values - everything from voltage_start onwards
    voltages = []
    for row in all_rows[voltage_start:]:
        if row and row[0].strip():
            try:
                voltages.append(float(row[0]))
            except ValueError:
                continue

    voltage_uv = np.array(voltages, dtype=np.float64)

    # Extract sample rate from metadata or use default
    # Handles formats: "512", "512 Hz", "512 Hertz"
    sample_rate = 512
    sr_raw = meta.get("sample_rate", "")
    if sr_raw:
        # Strip unit suffixes
        sr_clean = sr_raw.lower().replace("hertz", "").replace("hz", "").strip()
        try:
            sample_rate = int(float(sr_clean))
        except ValueError:
            pass

    # Average heart rate
    avg_hr = None
    hr_raw = meta.get("average_heart_rate", meta.get("averageheartrate", ""))
    if hr_raw:
        try:
            avg_hr = float(hr_raw.split()[0])  # Handle "72 bpm" format
        except (ValueError, IndexError):
            pass

    duration_s = len(voltage_uv) / sample_rate if sample_rate > 0 else 0

    return {
        "date": _parse_date(meta),
        "classification": _extract_classification(meta),
        "average_hr": avg_hr,
        "device": meta.get("device", meta.get("source", "Apple Watch")),
        "sample_rate": sample_rate,
        "voltage_uv": voltage_uv,
        "duration_s": duration_s,
        "num_samples": len(voltage_uv),
        "filepath": str(filepath),
        "metadata": meta,
    }


def parse_ecg_directory(dirpath: Path) -> list[dict]:
    """Parse all ECG CSV files in a directory, sorted by date.

    Looks for files matching ecg_*.csv or *.csv in the directory.
    """
    dirpath = Path(dirpath)
    if not dirpath.is_dir():
        raise NotADirectoryError(f"Not a directory: {dirpath}")

    csv_files = sorted(dirpath.glob("*.csv"))
    if not csv_files:
        return []

    results = []
    for f in csv_files:
        try:
            parsed = parse_ecg_csv(f)
            results.append(parsed)
        except Exception as e:
            print(f"Warning: Failed to parse {f.name}: {e}")

    # Sort by date if available
    results.sort(key=lambda x: x["date"] or datetime.min)
    return results


def extract_apple_health_zip(zip_path: Path, target_dir: Path) -> Path | None:
    """Extract Apple Health ZIP export, return path to electrocardiograms/ folder.

    The ZIP contains apple_health_export/electrocardiograms/ with ECG CSVs.
    """
    zip_path = Path(zip_path)
    target_dir = Path(target_dir)

    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as zf:
        # Find electrocardiogram files
        ecg_files = [
            n for n in zf.namelist()
            if "electrocardiogram" in n.lower() and n.endswith(".csv")
        ]

        if not ecg_files:
            return None

        ecg_dir = target_dir / "electrocardiograms"
        ecg_dir.mkdir(parents=True, exist_ok=True)

        for name in ecg_files:
            data = zf.read(name)
            out_name = Path(name).name
            (ecg_dir / out_name).write_bytes(data)

    return ecg_dir


def find_ecg_data(data_dir: Path) -> list[dict]:
    """Auto-detect and parse ECG data from the data directory.

    Handles:
    - ZIP files (Apple Health export)
    - electrocardiograms/ subdirectory
    - Individual CSV files in the directory
    """
    data_dir = Path(data_dir)
    results = []

    # Check for ZIP files
    for zf in data_dir.glob("*.zip"):
        try:
            ecg_dir = extract_apple_health_zip(zf, data_dir)
            if ecg_dir:
                results.extend(parse_ecg_directory(ecg_dir))
        except Exception as e:
            print(f"Warning: Failed to extract {zf.name}: {e}")

    # Check for electrocardiograms/ subdirectory
    ecg_subdir = data_dir / "electrocardiograms"
    if ecg_subdir.is_dir() and not results:
        results.extend(parse_ecg_directory(ecg_subdir))

    # Check for loose CSV files (only if no other ECG data found)
    if not results:
        csv_files = list(data_dir.glob("ecg_*.csv")) + list(data_dir.glob("ecg*.csv"))
        for f in csv_files:
            try:
                results.append(parse_ecg_csv(f))
            except Exception as e:
                print(f"Warning: Failed to parse {f.name}: {e}")

    # Deduplicate by filepath
    seen = set()
    deduped = []
    for r in results:
        if r["filepath"] not in seen:
            seen.add(r["filepath"])
            deduped.append(r)

    deduped.sort(key=lambda x: x["date"] or datetime.min)
    return deduped
