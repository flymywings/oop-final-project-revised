"""Turn raw sound files into the game's sounds/<event>.wav, and write sounds/SOURCES.md.

    python tools/process_sounds.py [--raw sounds/raw] [--out sounds]

Put one raw file per event in the raw folder, named <event>.<wav|ogg|mp3|flac>, plus
ORIGIN.txt with one line per file:   event | original file name | where it came from
Needs ffmpeg and ffprobe on PATH. For every file it:
  1. trims leading and trailing silence,
  2. converts to 44.1 kHz, 16-bit, stereo WAV,
  3. peak-normalises to -3 dB,
  4. measures the result and fails if the peak is above -1 dB (clipping risk),
  5. records the sha256 of the RAW file in SOURCES.md.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys

EVENTS = ("hover", "click", "light", "heavy", "special", "crit", "dodge", "miss",
          "block", "potion", "enemy_hit", "floor_clear", "victory", "defeat")
EXTENSIONS = (".wav", ".ogg", ".mp3", ".flac")
TARGET_PEAK_DB = -3.0
CLIP_LIMIT_DB = -1.0
TRIM = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.01,"
        "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.01,areverse")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def peak_db(path):
    """Loudest sample of a file in dB (ffmpeg volumedetect)."""
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "volumedetect",
               "-f", "null", "-"]).stderr
    match = re.search(r"max_volume:\s*(-?[\d.]+) dB", out)
    if not match:
        raise RuntimeError(f"cannot measure {path}")
    return float(match.group(1))


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        digest.update(handle.read())
    return digest.hexdigest()


def process(raw_path, out_path):
    """Trim, convert, normalise. Returns (peak_after_db, duration_seconds)."""
    trimmed = TRIM
    first = run(["ffmpeg", "-hide_banner", "-y", "-i", raw_path, "-af", trimmed,
                 "-ar", "44100", "-ac", "2", "-sample_fmt", "s16", out_path])
    if first.returncode != 0:
        raise RuntimeError(first.stderr[-400:])
    gain = TARGET_PEAK_DB - peak_db(out_path)
    tmp = out_path + ".tmp.wav"
    second = run(["ffmpeg", "-hide_banner", "-y", "-i", out_path, "-af", f"volume={gain:.2f}dB",
                  "-ar", "44100", "-ac", "2", "-sample_fmt", "s16", tmp])
    if second.returncode != 0:
        raise RuntimeError(second.stderr[-400:])
    os.replace(tmp, out_path)
    duration = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", out_path]).stdout.strip())
    return peak_db(out_path), duration


def read_origins(raw_dir):
    origins = {}
    path = os.path.join(raw_dir, "ORIGIN.txt")
    if os.path.exists(path):
        for line in open(path, encoding="utf8"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 3 and parts[0] in EVENTS:
                origins[parts[0]] = (parts[1], parts[2])
    return origins


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default="sounds/raw")
    parser.add_argument("--out", default="sounds")
    args = parser.parse_args()
    origins = read_origins(args.raw)
    rows, problems = [], []
    for event in EVENTS:
        raw = next((os.path.join(args.raw, event + ext) for ext in EXTENSIONS
                    if os.path.exists(os.path.join(args.raw, event + ext))), None)
        if raw is None:
            rows.append((event, "-", "NOT SOURCED", "-", "-", "-"))
            problems.append(f"{event}: no raw file")
            continue
        out = os.path.join(args.out, event + ".wav")
        peak, seconds = process(raw, out)
        if peak > CLIP_LIMIT_DB:
            problems.append(f"{event}: peak {peak} dB is too hot")
        name, origin = origins.get(event, ("?", "?"))
        if event not in origins:
            problems.append(f"{event}: missing line in ORIGIN.txt")
        rows.append((event, name, origin, sha256(raw), f"{peak:.1f} dB", f"{seconds:.2f} s"))
        print(f"{event:12s} peak {peak:6.1f} dB  {seconds:5.2f} s  <- {os.path.basename(raw)}")
    with open(os.path.join(args.out, "SOURCES.md"), "w", encoding="utf8") as handle:
        handle.write("# Sound sources\n\nThese effects are by Toby Fox (Undertale). They are used in a class project "
                     "and are not free-use.\n\n| Event | Original file | Origin | sha256 of the raw file | "
                     "Peak | Length |\n|---|---|---|---|---|---|\n")
        for row in rows:
            handle.write("| " + " | ".join(row) + " |\n")
    if problems:
        print("PROBLEMS:\n  " + "\n  ".join(problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
