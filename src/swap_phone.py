#!/usr/bin/env python3
"""Swap the site phone number everywhere in src/. Run ONLY after the Twilio number is actually owned.
Usage: python3 src/swap_phone.py && python3 src/build.py && python3 src/bundle_worker.py  (then redeploy)"""
import os, glob
OLD = [("(202) 688-5949", "(240) 226-3502"), ("+12026885949", "+12402263502")]
for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")):
    if f.endswith("swap_phone.py"): continue
    s = open(f).read(); n = s
    for a, b in OLD: n = n.replace(a, b)
    if n != s: open(f, "w").write(n); print("updated", os.path.basename(f))
