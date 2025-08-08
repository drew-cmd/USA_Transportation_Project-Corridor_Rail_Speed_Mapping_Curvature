#!/usr/bin/env python3
"""
map_curvature_avg_corridors.py
==============================
Creates a Folium map coloring **corridors** by average curvature-adjusted speed.
"""

import geopandas as gpd
import folium
from branca.colormap import linear

# ───── Config ─────
GPKG_FILE = "4 - Data_Corridor_Curve_Speed/corridors_with_curv_speed.gpkg"
LAYER     = "corridors"
MAP_FILE  = "Output/corridor_curvature_avg_map.html"

# ───── Load data ─────
print("▶︎ Loading corridor curvature summary …")
gdf = gpd.read_file(GPKG_FILE, layer=LAYER)
gdf_wgs = gdf.to_crs(epsg=4326)  # Folium requires WGS84

# Calculate estimated travel time in hours
gdf_wgs["est_travel_hr"] = gdf_wgs["total_length_mi"] / gdf_wgs["avg_curv_speed_mph"]

# ───── Colormap setup ─────
min_speed = gdf_wgs["avg_curv_speed_mph"].min()
max_speed = gdf_wgs["avg_curv_speed_mph"].max()

colormap = linear.RdYlGn_11.scale(min_speed, max_speed).to_step(10)
colormap.caption = "Avg Curvature-Adjusted Speed (mph)"

# ───── Create base map ─────
centroid = gdf_wgs.geometry.union_all().centroid
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6, tiles="CartoDB Positron")

# ───── Add corridors ─────
for _, row in gdf_wgs.iterrows():
    geom = row.geometry
    if geom is None or geom.is_empty or geom.geom_type != "LineString":
        continue

    coords_latlon = [(y, x) for x, y in geom.coords]
    color = colormap(row["avg_curv_speed_mph"])

    hours = int(row['est_travel_hr'])
    minutes = int(round((row['est_travel_hr'] - hours) * 60))
    
    popup_html = (
        f"<b>{row['from_to']}</b><br>"
        f"Avg Curv Adj Speed: {row['avg_curv_speed_mph']:.1f} mph<br>"
        f"Total Length: {row['total_length_mi']:.1f} mi<br>"
        f"Est Travel Time: {hours} hr {minutes} min"
    )

    folium.PolyLine(
        coords_latlon,
        color=color,
        weight=5,
        opacity=0.9,
        tooltip=folium.Tooltip(popup_html)
    ).add_to(m)

# ───── Add colormap legend ─────
colormap.add_to(m)

# ───── Save map ─────
m.save(MAP_FILE)
print(f"✔ Saved map → {MAP_FILE}")
