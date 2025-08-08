#!/usr/bin/env python3
"""
extract_routed_segments.py
==========================
Extracts geometries of used rail segments from graph + routing cache.
Outputs a GeoPackage with one row per segment used in routed corridors.
"""

import pickle
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
from pathlib import Path

GRAPH_FILE  = "1 - Data/graph_cache.pkl"
ROUTED_FILE = "1 - Data/routed_corridors_cache.pkl"
OUT_FILE    = "2 - Data_Segments/routed_segments.gpkg"
OUT_LAYER   = "segments"

def main():
    print("▶︎ Load graph and routed cache …")
    G, *_ = pickle.load(open(GRAPH_FILE, "rb"))
    routed = pickle.load(open(ROUTED_FILE, "rb"))

    rows = []
    for from_to, route in routed.items():
        if route is None: continue
        try:
            *_, line = route
        except Exception:  # fallback if format differs
            continue
        coords = list(line.coords)
        for a, b in zip(coords[:-1], coords[1:]):
            if G.has_edge(a, b):
                edge = G[a][b]
            elif G.has_edge(b, a):
                edge = G[b][a]
            else:
                continue
            geom = edge.get("geometry", LineString([a, b]))
            rows.append({
                "from_to": from_to,
                "geometry": geom,
                "length_mi": edge.get("length_mi"),
                "speed": edge.get("speed"),
                "type": edge.get("type")
            })

    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:5070")  # match your proj_crs
    gdf.to_file(OUT_FILE, layer=OUT_LAYER, driver="GPKG")
    print(f"✔ Saved {len(gdf)} segments → {OUT_FILE}")

if __name__ == "__main__":
    main()
