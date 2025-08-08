import geopandas as gpd

FILE = "2 - Data_Segments/routed_segments.gpkg"
LAYER = "segments"

gdf = gpd.read_file(FILE, layer=LAYER)

print("✅ File loaded.")
print(f"Number of segments: {len(gdf)}")
print("CRS:", gdf.crs)
print("\nColumns:", list(gdf.columns))
print("\nSample rows:")
print(gdf[["from_to", "length_mi", "speed", "type"]].head())

# Check for missing or bad geometries
print("\nMissing geometries:", gdf.geometry.isna().sum())
print("Invalid geometries:", (~gdf.geometry.is_valid).sum())
print("Empty geometries:", gdf.geometry.is_empty.sum())

# Check LineString types
geom_types = gdf.geometry.geom_type.value_counts()
print("\nGeometry types:\n", geom_types)

# Preview unique corridor names
print("\nUnique corridors:", gdf['from_to'].nunique())
print(gdf['from_to'].unique()[:10])
