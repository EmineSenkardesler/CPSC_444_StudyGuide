# Week 3: Coordinate Systems & Transformations
## Where Is "Here"?

**Difficulty**: ⭐⭐ Intermediate
**Time Estimate**: 2-3 hours
**Prerequisites**: Week 2 (continued): First Maps - you have used `.crs` and `.to_crs()` once already

---

## Overview

Last week you hit the trap: `field.area` gave `0.0003` and a warning. This week is the explanation. The Earth is round, your screen is flat, and a **coordinate reference system (CRS)** is the rule that says how the numbers in your data connect to real places on the ground. Pick the wrong one and your distances, areas and overlays go silently wrong. Pick the right one and it's a single line of code.

### What You'll Learn
- Why one dataset can have many different coordinate numbers for the same place
- The two kinds of CRS: **geographic** (degrees) and **projected** (meters)
- What an **EPSG code** is and the three codes you need for this course
- How to **check** a CRS and how to **convert** between them with `.to_crs()`
- What actually happens to your numbers, distances, areas and shapes when you convert
- The difference between `.set_crs()` (relabel) and `.to_crs()` (recalculate)

### Why This Matters
- Your GPS gives degrees. Your yield monitor may give UTM meters. Google Maps uses a third system. They have to meet somewhere.
- Every distance, area, buffer and "nearest neighbor" in this course is only correct in a projected CRS in meters.

---

## Learning Objectives

By the end of this week, you will be able to:
- [ ] Explain in one sentence why a flat map of a round Earth always distorts something
- [ ] Tell a geographic CRS (degrees) from a projected CRS (meters) by looking at the coordinates
- [ ] Recognize EPSG:4326, EPSG:32616 and EPSG:3857 and say what each is for
- [ ] Check the CRS of a GeoDataFrame and of a raster
- [ ] Convert a layer to another CRS with `.to_crs()` and predict what will change
- [ ] Choose the right CRS for storing, displaying and measuring

---

## Core Concepts

### 1. The Problem: Round Earth, Flat Map

**Simple explanation**: Try to flatten an orange peel onto a table. It tears or stretches. Every flat map is a stretched orange peel - somewhere, shapes, sizes or distances are distorted. There is no perfect map, only maps that are good enough for a particular job and place.

**A CRS is the recipe for the flattening**: which way the peel was cut, how it was stretched, and what units the result is measured in.

**Why it matters**: Two datasets made with two different recipes will not line up on the same map until you re-flatten one of them with the other's recipe. That re-flattening is a **transformation**, and it's what `.to_crs()` does.

---

### 2. Two Kinds of CRS

#### Geographic CRS - degrees on the globe
**What it is**: Positions as latitude and longitude, in degrees, on a model of the round Earth.

- **Example**: Urbana, IL is at **lon -88.2073, lat 40.1106**
- **The one you'll see everywhere**: **WGS 84 = EPSG:4326**. This is what GPS, phones and most web downloads give you.
- **Good for**: storing data, sharing data, plotting the whole world
- **Bad for**: measuring. A "degree" is not a fixed length.

**Why a degree is not a length**: 1° of latitude is about 111 km everywhere. But 1° of longitude shrinks as you go north - about 111 km at the equator, **about 85 km in Urbana**, and 0 km at the pole, where all the longitude lines meet. So "0.01 degrees" means different distances in different places, and "0.0003 square degrees" means nothing at all.

#### Projected CRS - meters on a flat sheet
**What it is**: The globe flattened onto a plane, with positions in **meters** (sometimes feet) east and north of an origin.

- **Example**: the same Urbana point is **x = 397110 m, y = 4440731 m** in UTM zone 16N
- **Good for**: distances, areas, buffers, anything you want to *measure*
- **Bad for**: only accurate inside its own region. Use an Illinois projection in Alaska and it's wrong again.

**How to tell them apart at a glance**: coordinates like `-88.2, 40.1` are degrees. Coordinates like `397110, 4440731` are meters. If your x values are between -180 and 180 and your y values between -90 and 90, you're in degrees.

---

### 3. EPSG Codes - the ID Numbers

**What it is**: Every CRS has a number, like a product code. You don't have to remember the math - you just say the number.

**The three you need in this course**:

- **EPSG:4326** - WGS 84, degrees. GPS, storage, sharing, world maps.
- **EPSG:32616** - UTM zone 16N, meters. Analysis and measurement in Illinois (and Indiana, Kentucky, western Michigan).
- **EPSG:3857** - Web Mercator, meters-but-distorted. What Google Maps and web tiles use. Fine for a background map, **never for areas**.

**Two more you may meet**:
- **EPSG:32615** - UTM zone 15N, for the western strip of Illinois (west of 90°W) and Iowa, Missouri, Minnesota.
- **EPSG:5070** - Albers Equal-Area for the whole continental US. Use it when you need correct areas across many states.

**How UTM zones work**: the world is cut into 60 vertical strips, each 6° of longitude wide, numbered from 1 to 60 going east. Illinois sits mostly in zone 16 (90°W to 84°W). Add "N" for the northern hemisphere. Look up any place at **epsg.io** - type a place name and it lists the codes.

---

### 4. Checking the CRS

**What it is**: Before you do anything with a spatial layer, ask it what its coordinates mean.

**Where the data comes from**: this page reuses the Week 2 example - the eight soil-sample sites and the simulated elevation raster. If you still have your Week 2 Colab notebook, `pts`, `field` and `elevation.tif` are already there and you can skip the next cell. Otherwise, run it once to create the two files (no download needed - the data is generated in code):

```python
!pip install -q rasterio
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import Polygon

# --- Week 2 sample sites -> samples.geojson ---
samples = pd.DataFrame({
    "site": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
    "lon":  [-88.237, -88.231, -88.225, -88.236, -88.229, -88.223, -88.234, -88.226],
    "lat":  [ 40.093,  40.094,  40.092,  40.099,  40.100,  40.098,  40.103,  40.103],
    "yield_bu_ac": [178, 185, 172, 190, 196, 181, 188, 175],
})
pts = gpd.GeoDataFrame(samples, geometry=gpd.points_from_xy(samples.lon, samples.lat), crs="EPSG:4326")
pts.to_file("samples.geojson", driver="GeoJSON")

# --- Week 2 field boundary ---
field = gpd.GeoDataFrame({"name": ["North field"]}, crs="EPSG:4326",
                         geometry=[Polygon([(-88.240, 40.090), (-88.220, 40.090), (-88.220, 40.105), (-88.240, 40.105)])])

# --- Week 2 simulated elevation -> elevation.tif ---
np.random.seed(444)
west, east, south, north = -88.245, -88.215, 40.085, 40.110
ncols, nrows = 60, 50
LON, LAT = np.meshgrid(np.linspace(west, east, ncols), np.linspace(north, south, nrows))
elev = (225 - 12 * (LON - west) / (east - west) + 6 * (LAT - south) / (north - south)
        + np.random.normal(0, 0.8, size=(nrows, ncols))).astype("float32")
transform = from_origin(west, north, (east - west) / ncols, (north - south) / nrows)
with rasterio.open("elevation.tif", "w", driver="GTiff", height=nrows, width=ncols, count=1,
                   dtype="float32", crs="EPSG:4326", transform=transform) as dst:
    dst.write(elev, 1)

print("created samples.geojson and elevation.tif")
```

**Now ask each layer what its coordinates mean**:

```python
# Vector layer - read it back from the file, the way you would with real data
pts = gpd.read_file("samples.geojson")
print(pts.crs)            # EPSG:4326  (or None - see Section 7)

# Raster
with rasterio.open("elevation.tif") as src:
    print(src.crs)        # EPSG:4326
    print(src.bounds)     # the numbers tell you degrees or meters
```

**Simple rule**: print the CRS of **every** layer the moment you load it. Layers that will be plotted or measured together must share the same CRS.

---

### 5. Converting with .to_crs()

**What it is**: Recalculating every coordinate in a layer from one CRS to another. The places stay where they are on the ground; only the numbers change.

```python
from shapely.geometry import Point

urbana = gpd.GeoSeries([Point(-88.2073, 40.1106)], crs="EPSG:4326")

urbana_utm = urbana.to_crs("EPSG:32616")   # meters, UTM 16N
urbana_web = urbana.to_crs("EPSG:3857")    # meters, Web Mercator

print(urbana.iloc[0])       # POINT (-88.2073 40.1106)
print(urbana_utm.iloc[0])   # POINT (397110.4 4440731.3)
print(urbana_web.iloc[0])   # POINT (-9819191.7 4882027.4)
```

**Same place, three sets of numbers.** None of them is "the true" coordinate - each is true inside its own system.

**It is reversible**:
```python
back = urbana_utm.to_crs("EPSG:4326")
print(back.iloc[0])         # POINT (-88.2073 40.1106) - right back where we started
```

**Works on whole layers**: `.to_crs()` converts every point, line and polygon in a GeoDataFrame at once, and keeps all the attribute columns.

```python
field_utm = field.to_crs("EPSG:32616")     # the Week 2 field boundary, now in meters
pts_utm   = pts.to_crs("EPSG:32616")       # the Week 2 sample sites, now in meters
```

---

### 6. What Actually Changes When You Convert

**Simple explanation**: Think of it as changing the ruler you hold up to the map, not moving anything on the map.

**What changes**:
- **The coordinate numbers** - degrees become meters (or vice versa).
- **The axis labels of your plot** - longitude/latitude become easting/northing.
- **The meaning of `.area`, `.distance()`, `.buffer()`** - in degrees they are nonsense, in meters they are real.
- **The apparent shape of large regions** - the whole US looks different in each system (see the figure). For a single field the shape barely changes, because the distortion is tiny over a few kilometers.

**What does not change**:
- **Where things are on the ground.** Site S1 is still S1.
- **Your attribute columns** - yields, names, dates all come along untouched.
- **The order and number of rows.**

**Real example - the Week 2 field**:
```python
print(field.area.iloc[0])                          # 0.0003     (square degrees - meaningless)
print(field.to_crs("EPSG:32616").area.iloc[0])     # 2,839,000  m²  ->  about 700 acres  (correct)
print(field.to_crs("EPSG:3857").area.iloc[0])      # 4,860,000  m²  ->  70% TOO BIG   (Web Mercator stretches Illinois)
```

Three "areas" for one field. Only the UTM one is real. That is the whole lesson in three lines.

**Real example - distance between two sample sites**:
```python
pts.geometry.iloc[0].distance(pts.geometry.iloc[1])        # 0.006  "degrees" - meaningless
pts_utm.geometry.iloc[0].distance(pts_utm.geometry.iloc[1])  # 523 m   - correct
```

---

### 7. set_crs() vs to_crs() - Relabel vs Recalculate

**The most common CRS mistake in this course.** They sound alike and do opposite things.

- **`.to_crs("EPSG:32616")`** - **recalculates** the numbers. "These are degrees; please turn them into UTM meters." Use this 95% of the time.
- **`.set_crs("EPSG:4326")`** - **only writes a label**. "These numbers are already degrees; I'm just telling you so." The numbers do not change. Use it only when a layer arrives with `crs = None` and you *know* what the numbers are.

```python
# A layer built from a plain table has no CRS yet
naive = gpd.GeoDataFrame(samples, geometry=gpd.points_from_xy(samples.lon, samples.lat))
print(naive.crs)                          # None

naive = naive.set_crs("EPSG:4326")        # RIGHT: the numbers are lon/lat, so label them as such
print(naive.crs)                          # EPSG:4326

utm = naive.to_crs("EPSG:32616")          # now convert for real
```

**What goes wrong if you mix them up**: `naive.set_crs("EPSG:32616")` would claim that `-88.2, 40.1` are *meters* - a point 88 meters west and 40 meters north of the UTM origin, somewhere in the Pacific Ocean. No error message. Just a wrong map.

**If `.to_crs()` complains "Cannot transform naive geometries"**: the layer has no CRS. Fix it with `.set_crs()` first - with the *correct* original code.

---

### 8. Rasters Have a CRS Too

**What it is**: A GeoTIFF stores its CRS and its corner position inside the file. Reprojecting a raster means re-drawing the grid in the new system, so it's a little more work than for vectors.

```python
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

with rasterio.open("elevation.tif") as src:                      # EPSG:4326 from Week 2
    dst_crs = "EPSG:32616"
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    profile = src.profile.copy()
    profile.update(crs=dst_crs, transform=transform, width=width, height=height)

    with rasterio.open("elevation_utm.tif", "w", **profile) as dst:
        reproject(source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
                  src_transform=src.transform, src_crs=src.crs,
                  dst_transform=transform, dst_crs=dst_crs,
                  resampling=Resampling.bilinear)

with rasterio.open("elevation_utm.tif") as src:
    print(src.crs, src.res)     # EPSG:32616, cell size now in meters (about 48 m x 48 m)
```

**Simple rule for this course**: reproject the *vector* layers to match the raster whenever you can - it's one line and loses nothing. Reproject the raster only when you need its cells in meters (for example, to compute slope).

---

### 9. Which CRS When - the Decision Rule

- **Storing or sharing data** → EPSG:4326 (degrees). Everyone can read it.
- **Plotting a whole country or the world** → EPSG:4326 for a quick look; EPSG:5070 (Albers) if areas must look right.
- **Measuring anything in Illinois** - distance, area, buffer, kriging, nearest neighbor → EPSG:32616 (UTM 16N).
- **Overlaying on a web basemap** → EPSG:3857, display only.
- **Two layers together** → whichever you pick, **both** must be in it. Convert the smaller one.

**Rule of thumb in one line**: **degrees to store and show, meters to measure, and always the same CRS for every layer on the map.**

---

## Course Materials

### Primary Notebooks

1. **[w01-exercises/Spatial_Plotting_python.ipynb](/tmp/cpsc444-study/w01-exercises/Spatial_Plotting_python.ipynb)**
   - Checking and converting the CRS of vector and raster layers
   - Plotting layers together after conversion

2. **[w01-exercises/Geospatial_Overlay_Tutorial.ipynb](/tmp/cpsc444-study/w01-exercises/Geospatial_Overlay_Tutorial.ipynb)**
   - Matching CRS before overlay
   - Extracting raster values under points and polygons

### Reference
- **epsg.io** - look up any CRS by name, place or code
- Your Week 2 notebook - `pts`, `field` and `elevation.tif` are the examples used on this page

---

## Key Commands at a Glance

```
gdf.crs                              # what do the numbers mean?
gdf.to_crs("EPSG:32616")             # RECALCULATE: degrees -> UTM meters (Illinois)
gdf.set_crs("EPSG:4326")             # RELABEL only: use when crs is None
src.crs, src.bounds, src.res         # the same questions for a raster
gdf.geometry.iloc[0].x               # peek at a coordinate to see degrees vs meters
```

### The Three Codes
```
EPSG:4326    degrees    store, share, world maps       (GPS gives you this)
EPSG:32616   meters     measure in Illinois            (UTM zone 16N)
EPSG:3857    meters*    web basemaps only              (*distorted - never for area)
```

### Sanity Numbers for Illinois
```
1° latitude   ≈ 111 km          1° longitude ≈ 85 km (at 40°N)
0.001°        ≈ 100 m           0.0001°      ≈ 10 m
UTM 16N x     ≈ 200,000 - 800,000 m     UTM 16N y ≈ 4,000,000 - 4,800,000 m
```

---

## Study Checkpoints

Before next week, make sure you can answer these questions:

### Can you explain...?

1. **Why can't a flat map show the Earth without distortion?**
   <details>
   <summary>Click to check your understanding</summary>
   The Earth is a curved surface and a map is flat. Flattening a curved surface always stretches or tears it somewhere (the orange-peel problem). Every projection trades off shape, area, distance or direction; a CRS is the specific trade-off you chose.
   </details>

2. **How can you tell from the numbers alone whether a layer is in degrees or meters?**
   <details>
   <summary>Click to check your understanding</summary>
   Degrees are small: x between -180 and 180, y between -90 and 90 (Illinois is around -88, 40). Meters are large: hundreds of thousands (UTM x around 400,000; y around 4,400,000). If in doubt, print `.crs`.
   </details>

3. **What is the difference between `.set_crs()` and `.to_crs()`?**
   <details>
   <summary>Click to check your understanding</summary>
   `.to_crs()` recalculates every coordinate into the new system - the numbers change, the places don't. `.set_crs()` only attaches a label and leaves the numbers alone - use it only when a layer has no CRS and you know what its numbers already are.
   </details>

4. **Why is Web Mercator (EPSG:3857) fine for a basemap but wrong for areas?**
   <details>
   <summary>Click to check your understanding</summary>
   Mercator keeps shapes and directions locally correct (good for navigating a map on screen) but stretches everything away from the equator. The Week 2 field comes out 70% too large in EPSG:3857. Use UTM (EPSG:32616) or Albers (EPSG:5070) for any area calculation.
   </details>

5. **You have a field boundary in EPSG:4326 and a yield raster in EPSG:32616. What do you do before overlaying them?**
   <details>
   <summary>Click to check your understanding</summary>
   Convert the field boundary with `field.to_crs("EPSG:32616")` so both layers share the raster's CRS (converting the vector is one line and lossless). Then plot or extract.
   </details>

### Can you do...?

1. **Print the CRS of a vector layer and a raster?**
   ```python
   print(gdf.crs)
   with rasterio.open("file.tif") as src:
       print(src.crs)
   ```

2. **Convert the Week 2 sample points to UTM and print the first coordinate in both systems?**
   ```python
   pts_utm = pts.to_crs("EPSG:32616")
   print(pts.geometry.iloc[0], pts_utm.geometry.iloc[0])
   ```

3. **Compute the distance between two sample sites in meters?**
   ```python
   pts_utm.geometry.iloc[0].distance(pts_utm.geometry.iloc[1])
   ```

4. **Fix a layer whose `.crs` is `None`?**
   ```python
   gdf = gdf.set_crs("EPSG:4326")      # only if you KNOW the numbers are lon/lat
   ```

### Self-Check Exercises

- [ ] Take the Week 2 `field` and compute its area in EPSG:32616, EPSG:3857 and EPSG:5070. Which two agree? Why?
- [ ] Convert `pts` to EPSG:32615 (zone 15N) instead of 16N and compare the distance S1-S2. It's close but not identical - why?
- [ ] Look up your hometown on epsg.io and write down its UTM zone code

### Ready for Next Week?

Check off each item:

- [ ] I can explain the round-Earth / flat-map problem in one sentence
- [ ] I know what EPSG:4326, EPSG:32616 and EPSG:3857 are for
- [ ] I print `.crs` before I overlay or measure anything
- [ ] I use `.to_crs("EPSG:32616")` before any distance or area in Illinois
- [ ] I know when `.set_crs()` is the right tool (and when it silently ruins a map)
- [ ] I can predict what changes and what doesn't when I convert a layer

**If you checked all items**: You're ready for next week - spatial sampling and interpolation (Kriging).

**If you're unsure about some items**: Redo Section 6 in Colab with the Week 2 field. Watching the three "areas" come out different is the fastest way to make this stick.

---

## Common Mistakes to Avoid

1. **Measuring in degrees**
   `.area`, `.distance()`, `.buffer()` on an EPSG:4326 layer give meaningless numbers (and a warning you should not ignore). Convert to EPSG:32616 first.

2. **Using `.set_crs()` when you meant `.to_crs()`**
   `.set_crs()` changes the label, not the numbers. Your points quietly move to the wrong side of the planet.

3. **Overlaying two layers in different CRS**
   They draw in different places or one is invisible. Print `.crs` for both; convert one.

4. **Using Web Mercator for areas**
   EPSG:3857 is for basemaps. Areas in Illinois come out about 70% too big.

5. **Wrong UTM zone**
   Zone 16N covers most of Illinois; the far western edge is zone 15N. Using a neighboring zone gives small errors, using a distant zone gives large ones. Check on epsg.io.

6. **Forgetting the raster**
   Vectors are easy to convert; rasters need `reproject`. Usually convert the vectors to match the raster, not the other way round.

---

## Tips for Success

1. **Print `.crs` first, every time.** Make it the first line after every `read_file` or `rasterio.open`.

2. **Peek at one coordinate.** `gdf.geometry.iloc[0]` tells you degrees vs meters in half a second.

3. **Remember three numbers.** 4326 to store, 32616 to measure, 3857 to display. Everything else you can look up.

4. **Convert the small layer to match the big one.** Points and polygons convert losslessly in one line; rasters are heavier.

5. **When a map looks wrong, suspect the CRS before you suspect the data.** It's the culprit nine times out of ten.

---

## Next Steps

Now that distances mean something:

→ **Next week**: spatial sampling and interpolation

You'll learn:
- Random, grid and stratified sampling designs
- Inverse-distance weighting (IDW)
- Variograms and Kriging - predicting values between your sample points
- Writing your prediction map out as a GeoTIFF

---

*A CRS is just an agreement about what the numbers mean. Make sure every layer on your map has signed the same agreement.*
