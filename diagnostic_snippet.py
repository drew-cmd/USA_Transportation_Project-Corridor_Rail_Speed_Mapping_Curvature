import geopandas as gpd

gdf = gpd.read_file("3 - Data_Segments_Curve/routed_segments_curv.gpkg")

# How many coords per segment?
gdf["n_coords"] = gdf.geometry.apply(lambda g: len(g.coords))

print("▶︎ Geometry coordinate counts:")
print(gdf["n_coords"].describe())

print("\n▶︎ Segments with less than 3 coords (can't compute curvature):")
print((gdf["n_coords"] < 3).sum(), "out of", len(gdf))

print("\n▶︎ Number of unique curv_speed_mph values:")
print(gdf["curv_speed_mph"].value_counts().head(10))
