#!/usr/bin/env python3
"""Build the slim web-serving JSON from the full-fidelity dataset.

The deployed galaxies175.json is a reduced-size derivative of
galaxies175.full.json so the Kinetics Lab explorer loads fast:
  - points per galaxy capped at 28 (stride downsampling, sorted by radius)
  - rounded: r_kpc to 2dp, velocities/errors to 1dp
  - compact key names: p=[v_inf, r_aff], c=[qag_red, mond_red, newt_red, qag_rms],
    f=bit flags (1=LOW_DOF, 2=r_aff pinned at 60)

The explorer (qag-kinetics-lab) reconstructs Newton / MOND / QAG curves
client-side from (r, v_baryon) + (v_inf, r_aff), so no information needed
for the curves is lost — only visual point density and decimal places.

Usage:  python3 build.py   # reads galaxies175.full.json, writes galaxies175.json
"""
import json

SRC = "galaxies175.full.json"
DST = "galaxies175.json"
CAP = 28


def slim(pts):
    if len(pts) <= CAP:
        return [[round(p[0], 2), round(p[1], 1), round(p[2], 1), round(p[3], 1)]
                for p in pts]
    stride = len(pts) / CAP
    return [[round(pts[int(i * stride)][0], 2), round(pts[int(i * stride)][1], 1),
             round(pts[int(i * stride)][2], 1), round(pts[int(i * stride)][3], 1)]
            for i in range(CAP)]


def main():
    full = json.load(open(SRC))
    out = {"galaxies": {}}
    for g in sorted(full["galaxies"]):
        f = full["galaxies"][g]
        flags = (1 if f["low_dof"] else 0) | (2 if f["pinned"] else 0)
        out["galaxies"][g] = {
            "p": [round(f["v_inf"], 1), round(f["r_aff"], 1)],
            "c": [round(f["qag_red"], 2), round(f["mond_red"], 2),
                  round(f["newt_red"], 1), round(f["qag_rms"], 2)],
            "f": flags,
            "pts": slim(f["pts"]),
        }
    json.dump(out, open(DST, "w"), separators=(",", ":"))
    import os
    print(f"wrote {DST}: {os.path.getsize(DST)//1024} KB, "
          f"{len(out['galaxies'])} galaxies")


if __name__ == "__main__":
    main()
