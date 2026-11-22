#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Programmatic validation of extracted ch10 images (no visual model needed).

Checks:
  - file exists, is a valid PNG
  - non-blank (has variance / multiple colors)
  - reasonable dimensions
  - for the map: has many distinct colors (map has labels/colors)
  - aspect ratio sanity
"""
import sys, os
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"translation-project/04_translation/v1/images"
files = ["ch10_p239_img0.png", "ch10_p245_img1.png"]

for f in files:
    p = os.path.join(BASE, f)
    print("====", f, "====")
    if not os.path.exists(p):
        print("  MISSING")
        continue
    im = Image.open(p).convert("RGB")
    w, h = im.size
    print("  size:", w, "x", h, "aspect %.3f" % (w / h))
    # sample colors
    colors = im.getcolors(maxcolors=1000000)
    ncolors = len(colors) if colors else ">1M"
    print("  distinct colors:", ncolors)
    # extrema per channel -> detect blank
    extrema = im.getextrema()
    print("  channel extrema:", extrema)
    # stddev via histogram
    import statistics
    px = list(im.getdata())
    # sample to keep it fast
    step = max(1, len(px) // 20000)
    sample = px[::step]
    for ci, name in enumerate("RGB"):
        vals = [s[ci] for s in sample]
        print("  %s mean=%.1f stdev=%.1f min=%d max=%d" % (
            name, statistics.mean(vals), statistics.pstdev(vals), min(vals), max(vals)))
    # verdict
    stdevs = [statistics.pstdev([s[ci] for s in sample]) for ci in range(3)]
    if max(stdevs) < 5:
        print("  VERDICT: WARNING low variance (possible blank)")
    else:
        print("  VERDICT: OK (content present)")
    print()