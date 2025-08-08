#!/usr/bin/env python3
"""
estimate_curvature_speed_per_segment.py
=======================================
Estimates curvature-adjusted speed for each rail segment based on geometry.
"""

from pathlib import Path
import numpy as np
import geopandas as gpd
from shapely.geometry import LineString
from tqdm import tqdm
from joblib import Parallel, delayed
from tqdm import tqdm

# ───── CONFIG ─────
INPUT_FILE  = "2 - Data_Segments/routed_segments.gpkg"
INPUT_LAYER = "segments"
OUTPUT_FILE = "3 - Data_Segments_Curve/routed_segments_curv.gpkg"
OUTPUT_LAYER = "segments"

Ea_in = 4.0     # Superelevation (inches)
Eu_in = 3.0     # Unbalanced superelevation (inches)
MAX_SPEED = 150 # mph

# ───── HELPER FUNCTIONS ─────
def compute_radius(p1, p2, p3):
    a = np.linalg.norm(p2 - p1)
    b = np.linalg.norm(p3 - p2)
    c = np.linalg.norm(p1 - p3)
    s = (a + b + c) / 2
    A = max(s * (s - a) * (s - b) * (s - c), 0.0) ** 0.5
    if A == 0: return np.inf
    return (a * b * c) / (4 * A)

def est_speed(radius_m):
    if radius_m == np.inf:
        return MAX_SPEED
    R_ft = radius_m * 3.28084
    speed = ((Ea_in + Eu_in) * R_ft / 11.8) ** 0.5
    return min(speed, MAX_SPEED)

def densify_line(line: LineString, spacing: float = 30.0):
    if line.length < spacing:
        return line
    num = max(3, int(line.length / spacing))
    return LineString([
        line.interpolate(float(d), normalized=False)
        for d in np.linspace(0, line.length, num)
    ])

def compute_avg_curv_speed(line: LineString):
    densified = densify_line(line)
    coords = np.array(densified.coords)
    if len(coords) < 3:
        return MAX_SPEED
    speeds = [
        est_speed(compute_radius(coords[i - 1], coords[i], coords[i + 1]))
        for i in range(1, len(coords) - 1)
    ]
    return float(np.mean(speeds)) if speeds else MAX_SPEED


# ───── MAIN ─────
def main():
    print("▶︎ Load segments …")
    gdf = gpd.read_file(INPUT_FILE, layer=INPUT_LAYER)

    print("▶︎ Estimating curvature-adjusted speeds in parallel …")
    segments = list(gdf.geometry)
    with tqdm(total=len(segments)) as pbar:
        def wrapped(g):
            result = compute_avg_curv_speed(g)
            pbar.update(1)
            return result

        curv_speeds = Parallel(n_jobs=-1, backend="threading")(delayed(wrapped)(g) for g in segments)

    gdf["curv_speed_mph"] = curv_speeds

    print("▶︎ Saving result …")
    gdf.to_file(OUTPUT_FILE, layer=OUTPUT_LAYER, driver="GPKG")
    print(f"✔ Saved → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
