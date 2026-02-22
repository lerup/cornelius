#!/usr/bin/env python3
"""Fetch Huberman Lab Toolkit episode transcripts from YouTube."""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os
import sys

TOOLKIT_EPISODES = {
    "h2aWYjSA1Jc": "Sleep Toolkit - Tools for Optimizing Sleep and Sleep-Wake Timing",
    "q1Ss8sTbFBY": "Fitness Toolkit - Protocol and Tools to Optimize Physical Health",
    "yb5zpo5WDG4": "Focus Toolkit - Tools to Improve Your Focus and Concentration",
    "CJIXbibQ0jI": "Mental Health Toolkit - Tools to Bolster Your Mood and Mental Health",
    "CrtR12PBKb0": "Goals Toolkit - How to Set and Achieve Your Goals",
    "ntfcfJ28eiU": "Tools for Managing Stress and Anxiety",
    "uuP-1ioh4LY": "Optimize Your Learning and Creativity with Science-Based Tools",
    "LYYyQcAJZfk": "Science-Supported Tools to Accelerate Your Fitness Goals",
}

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_transcript(video_id, title):
    """Fetch and save a single transcript."""
    safe_title = title.replace(" ", "_").replace("&", "and").replace("/", "-")
    output_path = os.path.join(OUTPUT_DIR, f"{safe_title}.md")

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=["en"])

        # Build markdown with timestamps
        lines = [f"# {title}\n"]
        lines.append(f"**Source:** https://www.youtube.com/watch?v={video_id}\n")
        lines.append("---\n")

        current_text = []
        current_start = None

        for entry in transcript:
            timestamp = entry.start
            text = entry.text.strip()

            if not text:
                continue

            # Group into ~60 second paragraphs for readability
            if current_start is None:
                current_start = timestamp

            current_text.append(text)

            if timestamp - current_start >= 60:
                mins = int(current_start // 60)
                secs = int(current_start % 60)
                paragraph = " ".join(current_text)
                lines.append(f"**[{mins:02d}:{secs:02d}]** {paragraph}\n")
                current_text = []
                current_start = None

        # Flush remaining
        if current_text and current_start is not None:
            mins = int(current_start // 60)
            secs = int(current_start % 60)
            paragraph = " ".join(current_text)
            lines.append(f"**[{mins:02d}:{secs:02d}]** {paragraph}\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"OK: {title} -> {os.path.basename(output_path)}")
        return True

    except Exception as e:
        print(f"FAIL: {title} -> {e}")
        return False

def main():
    print(f"Fetching {len(TOOLKIT_EPISODES)} toolkit transcripts...\n")

    success = 0
    failed = 0

    for video_id, title in TOOLKIT_EPISODES.items():
        if fetch_transcript(video_id, title):
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} succeeded, {failed} failed")

if __name__ == "__main__":
    main()
