#!/usr/bin/env python3
"""
aggregate_curvature_by_corridor.py
==================================
Aggregates average curvature-adjusted speed per corridor.
Outputs both CSV and GPKG.
"""

import geopandas as gpd
import pandas as pd

GPKG_IN = "3 - Data_Segments_Curve/routed_segments_curv.gpkg"
GEOJSON_IN = "3 - Data_Segments_Curve/corridor_routes.geojson"
SEGMENTS_LAYER = "segments"
OUT_CSV = "Output/corridor_curvature_summary.csv"
OUT_GPKG   = "4 - Data_Corridor_Curve_Speed/corridors_with_curv_speed.gpkg"

print("▶︎ Load routed segments …")
gdf = gpd.read_file(GPKG_IN, layer=SEGMENTS_LAYER)

#print(gdf.columns)

print("▶︎ Compute length-weighted curvature speed …")
summary = (
    gdf.groupby("from_to", group_keys=False)[["length_mi", "curv_speed_mph"]]
    .apply(lambda df: pd.Series({
        "total_length_mi": df["length_mi"].sum(),
        "avg_curv_speed_mph": (df["curv_speed_mph"] * df["length_mi"]).sum() / df["length_mi"].sum()
    }))
    .reset_index()
)

summary.to_csv(OUT_CSV, index=False)
print(f"✔ Saved: {OUT_CSV}")


corridors = gpd.read_file(GEOJSON_IN)
summary   = pd.read_csv("Output_terrain/corridor_curvature_summary.csv")

#print(corridors.columns)

# Merge on from_to
corridors = corridors.merge(summary, on="from_to", how="left")
corridors.to_file(OUT_GPKG, layer="corridors", driver="GPKG")
print(f"✔ Enriched corridors → {OUT_GPKG}")
