# USA Transportation Project Rail Speed Curvature Mapping

This project estimates curvature-adjusted rail speeds for U.S. passenger and freight corridors, starting from routed rail segments.
It processes each corridor’s path, calculates curvature-based speed limits for individual track segments, aggregates those speeds to the corridor level, and produces summary statistics and interactive maps.

---

## Project Structure
```
USA_TRANSPORTATION_PROJECT_RAIL_SPEED_CURVATURE_MAPPING/
├── 1 - Data/
│ ├── graph_cache.pkl
│ └── routed_corridors_cache.pkl
│
├── 2 - Data_Segments/
│ └── routed_segments.gpkg
│
├── 3 - Data_Segments_Curve/
│ ├── routed_segments_curv.gpkg
│ └── corridor_routes.geojson
│
├── 4 - Data_Corridor_Curve_Speed/
│ └── corridors_with_curv_speed.gpkg
│
├── Output/
│ ├── corridor_curvature_summary.csv
│ └── corridor_curvature_avg_map.html
│
├── extracted_routed_segments.py
├── inspect_routed_segments.py                  --generates no files
├── estimate_curvature_speed_per_segment.py
├── diagnostic_snippet.py                       --generates no files
├── aggregate_curvature_by_corridor.py
├── map_curvature_avg_corridors.py
├── LICENSE
├── NOTICE
├── README.md
├── .gitattributes
├── .gitignore
```

--

## Workflow Overview

The pipeline consists of five main processing stages:
    1. Extract routed rail segments
        Script: extracted_routed_segments.py
        - Loads previously routed corridors from graph_cache.pkl & routed_corridors_cache.pkl
        - Exports individual rail segments used in the routes to 2 - Data_Segments/routed_segments.gpkg
    2. Estimate curvature-adjusted speeds per segment
        Script: estimate_curvature_speed_per_segment.py
        - Reads routed_segments.gpkg
        - Calculates curve radius & applies superelevation-balance formulas
        - Writes routed_segments_curv.gpkg with per-segment curvature-based speed limits
    3. Inspect or debug segment curvature (optional)
        Scripts:
        - inspect_routed_segments.py — interactive checks of specific segments
        - diagnostic_snippet.py — debugging speed/geometry calculations
    4. Aggregate segment speeds to the corridor level
        Script: aggregate_curvature_by_corridor.py
        - Joins curvature-adjusted segment speeds back to corridor geometries
        - Produces corridors_with_curv_speed.gpkg with weighted average speeds per corridor
        - Outputs corridor_curvature_summary.csv with summary stats
    5. Map average corridor curvature-adjusted speeds
        Script: map_curvature_avg_corridors.py
        - Loads corridors_with_curv_speed.gpkg
        - Generates corridor_curvature_avg_map.html — an interactive Folium map colored by average curvature-adjusted speed

--

## Key Outputs

2 - Data_Segments/routed_segments.gpkg – Raw routed rail segments from graph routing

3 - Data_Segments_Curve/routed_segments_curv.gpkg – Same segments with curvature speed limits added

3 - Data_Segments_Curve/corridor_routes.geojson – Routed corridors in GeoJSON format for visualization

4 - Data_Corridor_Curve_Speed/corridors_with_curv_speed.gpkg – Corridor geometries with average curvature speed stats

Output/corridor_curvature_summary.csv – Per-corridor summary table (length, avg curvature speed, etc.)

Output/corridor_curvature_avg_map.html – Folium map showing corridors colored by curvature-adjusted average speed

---

## Requirements

Install required packages via pip:

```bash
pip install geopandas shapely pyproj pandas folium tqdm math scipy
```

Other system-level requirements:

GDAL/OGR (for reading shapefiles)

---

### How to Run

Run the main script:

```
python extracted_routed_segments.py
python estimate_curvature_speed_per_segment.py
python aggregate_curvature_by_corridor.py
python map_curvature_avg_corridors.py

```

Optional: Use inspect_routed_segments.py or diagnostic_snippet.py for debugging intermediate results.


### Notes

Speed Model:
    - Curvature speed limits are calculated using a superelevation-balance formula with assumed equilibrium & unbalanced superelevation values
    - This does not include acceleration/deceleration or dwell time at stations — it reflects track geometry-limited running speeds only
Caching:
    - graph_cache.pkl and routed_corridors_cache.pkl come from the corridor routing step in the Mapping Foundation repo
    - These caches prevent re-running expensive route computations
Visualization:
    - All maps are in WGS84 (EPSG:4326) for web display
    - GPKG and CSV outputs are in projected CRS for accurate length/speed calculations

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

### Data Sources

- Routed corridors & graph caches
- Amtrak & freight rail shapefiles from NTAD
- Metro anchors from Census TIGER/Line + ACS

The datasets used in this project originate from U.S. government sources (e.g., NTAD, TIGER/Line, ACS) and are in the public domain under 17 U.S.C. § 105.

For more information, see the [`NOTICE`](NOTICE) file.

