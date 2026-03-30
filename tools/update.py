#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob, os, subprocess, sys
from datetime import datetime

SOURCES = {
  "renfeld":   "https://ssl.renfe.com/gtransit/Fichero_AV_LD/google_transit.zip",
  "cercanias": "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip",
}

def latest_zip(basename):
  matches = sorted(glob.glob(f"data/{basename}_????-??-??_??-??.zip"))
  return matches[-1] if matches else None

def run_dump(basename, url):
  ts       = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
  output   = f"data/{basename}_{ts}.zip"
  existing = latest_zip(basename)

  cmd = [sys.executable, "tools/gtfs_dump.py", url, output]
  if existing:
    cmd += ["--input", existing]

  print(f"\n[{basename}] {existing or '(no local file)'} -> {output}")
  return subprocess.run(cmd).returncode == 0

os.makedirs("data", exist_ok=True)
failures = [b for b, u in SOURCES.items() if not run_dump(b, u)]

print()
if failures:
  print(f"Failed: {', '.join(failures)}", file=sys.stderr)
  sys.exit(1)
print("Done.")

