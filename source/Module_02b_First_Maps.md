# Module 02 (continued): First Maps
## Vector & Raster Data in Python - Week 2 Continuation

**Difficulty**: ⭐⭐ Intermediate
**Time Estimate**: 3-4 hours
**Prerequisites**: Module 01 (Python basics, plotting), Module 02 (simple & multiple regression)

---

## Module Overview

Everything you did in Weeks 1-2 was a table of numbers - yields, rainfall, temperatures. This continuation adds two columns to that table - **longitude and latitude** - and the table becomes a map. You'll learn the two ways computers store "where" (vector and raster), how to draw both in Python, and why a map can reveal a problem that a regression alone cannot see.

### What You'll Learn
- What makes spatial data different from the tables you used in Weeks 1-2
- Vector data (points, lines, polygons) vs raster data (grids of cells)
- How to build a map from a plain table of coordinates
- What a Coordinate Reference System (CRS) is, and why area and distance go wrong without one
- How to create, save, load and plot a raster (GeoTIFF)
- How to pull raster values out at sample points and feed them into regression

### Why This Matters
Almost every dataset in agriculture has a location attached:
- Soil samples come from specific spots in a field
- Yield monitors record a value every few meters
- Satellite images are grids of pixels covering the landscape
- Field boundaries, counties and management zones are shapes

Module 02 warned that regression assumes **independent errors** - and nearby locations tend to share the same errors. Before we can **fix** that (Modules 03-04), we need to be able to **see** it. That means maps.

---

## Learning Objectives

By the end of this module, you will be able to:
- [ ] Distinguish vector data from raster data and give an agricultural example of each
- [ ] Build a GeoDataFrame from a plain table of coordinates and plot it, coloring points by an attribute
- [ ] Create a polygon (a field boundary) from a list of coordinates and overlay it with points
- [ ] Explain what a CRS is, check it with `.crs`, and convert degrees to meters with `.to_crs()` before measuring
- [ ] Load real vector data from a file or URL, filter it, and make a choropleth map
- [ ] Create, plot, save (GeoTIFF) and re-open a raster with NumPy and rasterio, and overlay vector layers on it
- [ ] Extract raster values at point locations and connect the result to regression from Module 02

---

## Core Concepts

### 1. From a Table to a Map

**What it is**: Spatial data is ordinary data plus a location.

**Simple explanation**: Here is the kind of table you used in Weeks 1-2:

```
site   yield (bu/ac)
S1     178
S2     185
S3     172
```

Ask: **"Where is the good soil?"** You can't answer - nothing says where S1 is. Add two columns:

```
site   lon        lat       yield (bu/ac)
S1     -88.237    40.093    178
S2     -88.231    40.094    185
S3     -88.225    40.092    172
```

That's it. That is spatial data. Everything from Module 01 (lists, dictionaries, loops, if/else) and Module 02 (mean, regression) still applies. What's new is that location lets us ask a question the old table couldn't: **are nearby things alike?**

**Why it matters**: In a field, high-yield sites cluster together (good drainage, better soil), and so do low-yield sites. That clustering is information - and it's also exactly what breaks the "independent errors" assumption of regression.

---

### 2. Raster vs Vector Data

Think of this like the difference between a photo and a drawing.

#### Vector Data (Like a Drawing)
**What it is**: Shapes defined by coordinates - **points**, **lines** or **polygons** - each with a row of attributes attached.

- **Points**: soil-sample sites, weather stations, individual trees
- **Lines**: roads, rivers, tile-drain lines
- **Polygons**: field boundaries, counties, management zones

**In Python**: `geopandas` - a pandas DataFrame with one extra column called `geometry`, plus a CRS.

**File formats**: Shapefile (.shp), GeoPackage (.gpkg), GeoJSON (.geojson)

#### Raster Data (Like a Photo)
**What it is**: Space divided into a grid of equal cells (pixels), each holding one value.

- Elevation model (DEM): each cell = height in meters
- Satellite NDVI: each cell = how green the crop is
- Rainfall surface, temperature surface, yield-monitor map

**In Python**: `rasterio` reads and writes the file; the values are a plain NumPy 2D array - the same array you built in the "first raster" exercise of Module 01.

**File format**: GeoTIFF (.tif) - an image file that also stores its CRS and position on Earth.

#### When to Use Each
- **Vector** for discrete things with precise edges and attributes (a field, a sample site)
- **Raster** for continuous things that vary everywhere (elevation, temperature, greenness)

Zoom into a drawing and the lines stay crisp; zoom into a photo and you see pixels. Same trade-off here.

---

### 3. Setting Up in Google Colab

**What it is**: The libraries for this module. `geopandas` and `shapely` come pre-installed in Colab; `rasterio` usually does not, so the first cell installs it.

```python
# Run this cell first (re-run after every runtime restart)
!pip install -q rasterio

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import rasterio
from rasterio.transform import from_origin
from rasterio.plot import show

print(gpd.__version__, rasterio.__version__)
```

**Why it matters**: Nothing else in this module runs without these imports. If you see `ModuleNotFoundError: rasterio`, you skipped this cell.

---

### 4. Vector Data I: Points from a Plain Table

**What it is**: Turning a DataFrame with lon/lat columns into a **GeoDataFrame** - the same table with a `geometry` column and a CRS.

**Real-world example**: Eight soil-sample sites in a corn field near Urbana, each with a measured yield.

```python
samples = pd.DataFrame({
    "site":        ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
    "lon":         [-88.237, -88.231, -88.225, -88.236, -88.229, -88.223, -88.234, -88.226],
    "lat":         [ 40.093,  40.094,  40.092,  40.099,  40.100,  40.098,  40.103,  40.103],
    "yield_bu_ac": [178, 185, 172, 190, 196, 181, 188, 175],
})

# Same table + a geometry column + a CRS
pts = gpd.GeoDataFrame(
    samples,
    geometry=gpd.points_from_xy(samples.lon, samples.lat),
    crs="EPSG:4326",          # lon/lat in degrees - what a GPS gives you
)

pts.head()
print(pts.crs)          # EPSG:4326 (WGS 84)
pts.geometry.x          # the longitude of each point, pulled back out
```

It **looks like** a DataFrame - because it is one. Every pandas skill from Module 01 works on it.

**Your first map**:

```python
ax = pts.plot(column="yield_bu_ac", cmap="YlGn", legend=True,
              markersize=120, edgecolor="black", figsize=(6, 6))

# Label each point - the same for/zip loop pattern from Module 01
for x, y, label in zip(pts.geometry.x, pts.geometry.y, pts.site):
    ax.annotate(label, (x, y), xytext=(5, 5), textcoords="offset points")

ax.set_title("Corn yield at soil-sample sites")
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
plt.show()
```

**Why it matters**: `.plot(column=...)` colors features by an attribute - the map version of a colorbar. The rule from Module 01 still holds: **title, axis labels, legend**, always.

Look at the map: where are the high yields? They cluster in the north-center. Hold that thought.

---

### 5. Vector Data II: Polygons and Coordinate Reference Systems

#### Building a Polygon
**What it is**: A closed shape from a list of corner coordinates - here, a field boundary.

```python
# (lon, lat) corners; the polygon closes itself automatically
corners = [(-88.240, 40.090), (-88.220, 40.090), (-88.220, 40.105), (-88.240, 40.105)]

field = gpd.GeoDataFrame({"name": ["North field"]},
                         geometry=[Polygon(corners)], crs="EPSG:4326")

fig, ax = plt.subplots(figsize=(6, 6))
field.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=2)   # layer 1
pts.plot(ax=ax, column="yield_bu_ac", cmap="YlGn", legend=True,       # layer 2
         markersize=120, edgecolor="black")
ax.set_title("North field with sample sites")
plt.show()
```

**The layering pattern**: create `fig, ax` once, then call each layer's `.plot(ax=ax, ...)`. Layers stack in the order you draw them.

#### The CRS Trap
**What it is**: A **Coordinate Reference System (CRS)** says what the coordinate numbers mean. EPSG:4326 means "degrees of longitude and latitude on the globe."

**Simple explanation**: Ask "how big is this field?" and run:

```python
field.area          # 0.0003 ... plus a warning.  0.0003 WHAT?
```

Degrees are not a unit of area. One degree of longitude is about 85 km in Illinois but about 0 km at the North Pole. To measure anything, you need a **projected CRS** in meters. For Illinois that is UTM zone 16N = **EPSG:32616**.

```python
field_utm = field.to_crs("EPSG:32616")
area_acres = field_utm.area.iloc[0] / 4046.86
print(f"Field area: {area_acres:.0f} acres")      # about 700 acres

pts_utm = pts.to_crs("EPSG:32616")
d = pts_utm.geometry.iloc[0].distance(pts_utm.geometry.iloc[1])
print(f"S1 to S2: {d:.0f} m")                     # about 520 m
```

**Rules of thumb**:
- **Always check `.crs` first.** Two layers must share a CRS before you overlay or measure them.
- **Degrees for storing and displaying; meters for measuring.** `.to_crs()` converts.
- If `.crs` is `None`, geopandas cannot convert. Declare it with `.set_crs("EPSG:4326")` - but only if you **know** that's what the numbers are.

**Why it matters**: Every "my areas are wrong" and "my layers don't line up" problem in this course is a CRS problem. Module 03 goes deeper; this is the habit to build now.

---

### 6. Vector Data III: Loading Real Data

**What it is**: `gpd.read_file()` opens shapefiles, GeoPackages, GeoJSON - from disk or straight from a URL.

**Real-world example**: US state boundaries with population density.

```python
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
states = gpd.read_file(url)
print(states.crs, states.shape)
states.head()

# A choropleth: polygons colored by an attribute - same column= argument as for points
ax = states.plot(column="density", cmap="OrRd", legend=True,
                 edgecolor="white", linewidth=0.3, figsize=(9, 5))
ax.set_xlim(-130, -65); ax.set_ylim(23, 50)     # crop out Alaska / Hawaii / PR
ax.set_title("Population density by state")
plt.show()
```

Filtering is plain pandas - a Module 01 skill:

```python
il = states[states["name"] == "Illinois"]

ax = il.plot(facecolor="lightgrey", edgecolor="black", figsize=(4, 6))
pts.plot(ax=ax, color="red", markersize=30)
ax.set_title("Our sample sites in Illinois")
plt.show()
```

**Think about it**: Why do our 8 points look like a single dot? Scale - 700 acres on a state map. Zoom with `ax.set_xlim()` / `ax.set_ylim()`.

---

### 7. Raster Data: Create, Plot, Save, Read Back

#### Build a Raster with Real Coordinates
**What it is**: The 2D NumPy array from Module 01's "first raster" exercise, but now anchored to real longitude/latitude.

```python
np.random.seed(444)
west, east, south, north = -88.245, -88.215, 40.085, 40.110    # covers the field
ncols, nrows = 60, 50

lon = np.linspace(west, east, ncols)
lat = np.linspace(north, south, nrows)   # north FIRST: rasters store the top row first, like an image
LON, LAT = np.meshgrid(lon, lat)

# A gently tilted "elevation" surface: higher in the north-west, plus noise
elev = (225
        - 12 * (LON - west) / (east - west)
        +  6 * (LAT - south) / (north - south)
        + np.random.normal(0, 0.8, size=(nrows, ncols))).astype("float32")

plt.imshow(elev, cmap="terrain", extent=[west, east, south, north])
plt.colorbar(label="Elevation (m)")
plt.title("Simulated elevation (m)")
plt.xlabel("Longitude"); plt.ylabel("Latitude")
plt.show()
```

**Key ideas**:
- `extent=` is what turns "an image" into "a map": it tells matplotlib the coordinates of the corners.
- `elev[0, 0]` is the **north-west** cell; `elev[-1, -1]` is the south-east. Row index increases going south.

#### Save It as a GeoTIFF
**What it is**: A GeoTIFF is an image file that carries its own CRS and position - so anyone who opens it knows where on Earth it belongs.

```python
xres = (east - west) / ncols
yres = (north - south) / nrows
transform = from_origin(west, north, xres, yres)   # top-left corner + cell size

with rasterio.open("elevation.tif", "w", driver="GTiff",
                   height=nrows, width=ncols, count=1, dtype="float32",
                   crs="EPSG:4326", transform=transform) as dst:
    dst.write(elev, 1)
```

#### Read It Back and Overlay Everything
**What it is**: Exactly how you would open a real DEM or satellite image - then stack the vector layers on top.

```python
with rasterio.open("elevation.tif") as src:
    print(src.crs, src.shape, src.res)
    print(src.bounds)

    fig, ax = plt.subplots(figsize=(7, 6))
    show(src, ax=ax, cmap="terrain")                                     # raster layer
    field.plot(ax=ax, facecolor="none", edgecolor="white", linewidth=2)  # polygon layer
    pts.plot(ax=ax, column="yield_bu_ac", cmap="YlGn",                   # point layer
             edgecolor="black", markersize=120, legend=True)
    ax.set_title("Yield samples over elevation")
    plt.show()
```

**Why it matters**: Three layers on one map works **only** because all three share EPSG:4326. The `with rasterio.open(...) as src:` block is like opening a book: read what you need inside it, and it closes itself afterwards. `src.read(1)` hands you the plain NumPy array back, so `.mean()`, comparisons and slicing from Module 01 all work.

---

### 8. Connecting Maps to Regression

**What it is**: Pulling the raster value out from under each sample point, so "does yield depend on elevation?" becomes a two-column table that Module 02 already knows how to handle.

```python
coords = list(zip(pts.geometry.x, pts.geometry.y))      # [(lon, lat), ...]

with rasterio.open("elevation.tif") as src:
    pts["elev_m"] = [value[0] for value in src.sample(coords)]

pts[["site", "yield_bu_ac", "elev_m"]]
```

Now Module 02 takes over:

```python
from scipy import stats

fit = stats.linregress(pts.elev_m, pts.yield_bu_ac)
print(f"slope = {fit.slope:.2f} bu/ac per m,  R² = {fit.rvalue**2:.2f},  p = {fit.pvalue:.2f}")

plt.scatter(pts.elev_m, pts.yield_bu_ac)
plt.plot(pts.elev_m, fit.intercept + fit.slope * pts.elev_m, "--")
plt.xlabel("Elevation (m)"); plt.ylabel("Yield (bu/ac)")
plt.title("Yield vs elevation at 8 sample sites")
plt.show()
```

With the seed above: slope about 2.0, R² about 0.28, p about 0.17 - weak, as it should be with 8 points.

**Now map the residuals** - the part of yield the regression could not explain:

```python
pts["resid"] = pts.yield_bu_ac - (fit.intercept + fit.slope * pts.elev_m)

fig, ax = plt.subplots(figsize=(6, 6))
field.plot(ax=ax, facecolor="none", edgecolor="black")
pts.plot(ax=ax, column="resid", cmap="RdBu", vmin=-12, vmax=12,
         legend=True, markersize=160, edgecolor="black")
for x, y, r in zip(pts.geometry.x, pts.geometry.y, pts.resid):
    ax.annotate(f"{r:+.0f}", (x, y), xytext=(6, 6), textcoords="offset points")
ax.set_title("Regression residuals (blue = yield higher than elevation predicts)")
plt.show()
```

**Why it matters**: The residuals are not scattered at random. The blues sit together in the north-center; the reds sit at the edges. Nearby sites share what the model missed - drainage, soil type, a wet spot. That is a violation of assumption #2 in Module 02, **independence of errors**. Ordinary regression does not know the sites have locations. **Every method from Module 03 onward - variograms, kriging, spatial autocorrelation - is a way of putting the map back into the statistics.**

---

## In-Class Activity: Think-Pair-Share

**"Is this a regression problem or a map problem?"** (about 10 minutes)

**Purpose**: Connect Module 01 (data structures), Module 02 (regression assumptions) and this module (maps) into one insight: **location is information the regression is ignoring.**

**On screen**: the yield-over-elevation map (Section 7) next to the scatter plot with the regression line (Section 8).

**Think - 2 minutes, alone, write it down**:

1. **(Module 01)** If you had to store ONE sample site - its name, lon, lat and yield - in plain Python, would you use a list, a tuple or a dictionary? What does a GeoDataFrame add on top of a whole table of those?

2. **(Module 02)** Module 02 listed five regression assumptions. Look at the **map**, not the scatter plot. Which assumption are you least sure about here - and what on the map makes you doubt it?

**Pair - 3 minutes**: Compare answers with a neighbor. Together, finish this sentence with a number and a word:

"Two sample sites ___ m apart probably have ___ (more / less) similar yields than two sites 1 km apart, so the regression errors are probably ___ (independent / not independent)."

**Share - 5 minutes**: Two or three pairs report out. Then the residual map from Section 8 is revealed.

**The take-away**: A `dict` per site is the natural Module 01 answer; a GeoDataFrame is a table of those **plus** a CRS and geometry methods (`.to_crs`, `.area`, `.distance`, `.plot`). Same data, more power. And the residual map shows spatial clustering - the independence assumption is broken, and that is the problem the rest of the course solves.

**Alternative format - Quescussion** (if the room is quiet): 5 minutes; you may only speak in **questions**, no statements, and each question must build on the previous one. Seed question: **"If two neighboring sites both have high residuals, is that a coincidence?"**

---

## Practice Exercises

Each exercise reuses `pts`, `field` and `elevation.tif` from the sections above. Submit a Colab link.

### Exercise 1 - Your Own Layer (Module 01 skills: lists, loops)

Create a list of 5 tuples `(name, lon, lat, value)` for imaginary weather stations anywhere inside the raster extent (lon -88.245 to -88.215, lat 40.085 to 40.110). Turn them into a GeoDataFrame (`crs="EPSG:4326"`) and plot them **on top of** the elevation raster together with the field boundary. Label each station with its name.

<details>
<summary>Click to check a solution</summary>

```python
stations = [("W1", -88.243, 40.108, 21.5), ("W2", -88.230, 40.087, 22.1),
            ("W3", -88.218, 40.107, 20.9), ("W4", -88.235, 40.097, 21.8),
            ("W5", -88.222, 40.093, 22.4)]
wdf = pd.DataFrame(stations, columns=["name", "lon", "lat", "temp_c"])
wx = gpd.GeoDataFrame(wdf, geometry=gpd.points_from_xy(wdf.lon, wdf.lat), crs="EPSG:4326")

with rasterio.open("elevation.tif") as src:
    fig, ax = plt.subplots(figsize=(7, 6))
    show(src, ax=ax, cmap="terrain")
    field.plot(ax=ax, facecolor="none", edgecolor="white", linewidth=2)
    wx.plot(ax=ax, color="red", marker="^", markersize=100, edgecolor="black")
    for x, y, n in zip(wx.geometry.x, wx.geometry.y, wx.name):
        ax.annotate(n, (x, y), xytext=(5, 5), textcoords="offset points", color="white")
    ax.set_title("Weather stations over elevation")
    plt.show()
```
</details>

### Exercise 2 - Buffers Need Meters (CRS)

Draw a **150 m** circle around every sample site. Hint: `.buffer()` uses the units of the CRS, so convert to EPSG:32616 first, buffer, then convert back to EPSG:4326 to plot over the field. In a text cell, explain what happens if you call `pts.buffer(150)` **without** converting, and why.

<details>
<summary>Click to check a solution</summary>

```python
rings = pts.to_crs("EPSG:32616").buffer(150).to_crs("EPSG:4326")

fig, ax = plt.subplots(figsize=(6, 6))
field.plot(ax=ax, facecolor="none", edgecolor="black")
rings.plot(ax=ax, color="steelblue", alpha=0.3)
pts.plot(ax=ax, color="black", markersize=15)
ax.set_title("150 m buffers around sample sites")
plt.show()
```
Without converting, 150 is interpreted as 150 **degrees** - circles bigger than the planet (geopandas warns you).
</details>

### Exercise 3 - An If/Else for Every Cell (raster + Module 01 logic)

Read `elevation.tif`, compute the mean elevation, and make a new raster that is `True` where elevation is above the mean and `False` elsewhere. Plot it in grey (`cmap="Greys"`) with the correct `extent`. In a text cell: what fraction of cells are "high"? (Hint: `.mean()` of a True/False array.) Explain in one sentence how `elev > elev.mean()` relates to the `if/else` you wrote in Module 01.

<details>
<summary>Click to check a solution</summary>

```python
with rasterio.open("elevation.tif") as src:
    elev = src.read(1)
    b = src.bounds

high = elev > elev.mean()
print(f"{high.mean():.0%} of cells are above the mean")   # about 50%

plt.imshow(high, cmap="Greys", extent=[b.left, b.right, b.bottom, b.top])
plt.title("Cells above mean elevation"); plt.xlabel("Longitude"); plt.ylabel("Latitude")
plt.show()
```
`elev > elev.mean()` applies the same "if value > threshold: True, else False" decision to all 3,000 cells at once - vectorized, no loop needed.
</details>

### Exercise 4 - Which Sites Sit High? (join everything)

Using `pts["elev_m"]` from Section 8, write a `for` loop with an `if/elif/else` that prints, for each site, whether it is `"high"` (above 223 m), `"mid"` (220-223 m) or `"low"` (below 220 m). Add that label as a new column and plot the points colored by category (hint: `pts.plot(column="zone", categorical=True, legend=True)`). Compare with the yield map: do the zones line up with yield?

<details>
<summary>Click to check a solution</summary>

```python
zones = []
for site, e in zip(pts.site, pts.elev_m):
    if e > 223:
        z = "high"
    elif e >= 220:
        z = "mid"
    else:
        z = "low"
    print(site, round(e, 1), z)
    zones.append(z)
pts["zone"] = zones

fig, ax = plt.subplots(figsize=(6, 6))
field.plot(ax=ax, facecolor="none", edgecolor="black")
pts.plot(ax=ax, column="zone", categorical=True, legend=True, markersize=140, edgecolor="black")
ax.set_title("Elevation zone of each sample site")
plt.show()
```
</details>

---

## Course Materials

### Primary Notebooks

1. **[w01-exercises/Spatial_Plotting_python.ipynb](/tmp/cpsc444-study/w01-exercises/Spatial_Plotting_python.ipynb)**
   - Loading and visualizing rasters with rasterio
   - Working with geopandas for vector data
   - Basic spatial plotting

2. **[w01-exercises/Geospatial_Overlay_Tutorial.ipynb](/tmp/cpsc444-study/w01-exercises/Geospatial_Overlay_Tutorial.ipynb)**
   - Overlaying vector and raster data
   - Extracting raster values at points and inside polygons

3. **[w01-exercises/TrialDesign_SpatialMapping_Tutorial.ipynb](/tmp/cpsc444-study/w01-exercises/TrialDesign_SpatialMapping_Tutorial.ipynb)**
   - Mapping a field trial
   - Visualizing treatment effects spatially

---

## Key Commands at a Glance

### Vector (geopandas)
```
gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
gpd.read_file("file.shp")          # also .gpkg, .geojson, or a URL
gdf.crs                            # what do the coordinates mean?
gdf.to_crs("EPSG:32616")           # degrees -> meters (UTM 16N, Illinois)
gdf.plot(column="attr", legend=True, ax=ax)
gdf.area, gdf.buffer(150), a.distance(b)     # only meaningful in a projected CRS
```
**In words**: build or read a layer, check its CRS, convert to meters before measuring, plot with `ax=` to stack layers.

### Raster (rasterio + numpy)
```
with rasterio.open("file.tif") as src:
    arr = src.read(1)              # band 1 as a NumPy array
    src.crs, src.bounds, src.res   # where it is and how fine the cells are
    show(src, ax=ax)               # draw it in real coordinates
    src.sample([(lon, lat), ...])  # values under points
plt.imshow(arr, extent=[west, east, south, north])
```
**In words**: open, read the array, check CRS and bounds, draw with `show()` or `imshow(extent=...)`, sample under points.

### CRS Codes You Will Use
```
EPSG:4326   degrees (WGS 84) - GPS, storage, display
EPSG:32616  meters (UTM zone 16N) - Illinois analysis
EPSG:3857   Web Mercator - what web maps use
```

---

## Study Checkpoints

Before moving to Module 03, make sure you can answer these questions:

### Can you explain...?

1. **What's the difference between vector and raster data? Give an agricultural example of each.**
   <details>
   <summary>Click to check your understanding</summary>
   Vector = shapes (points, lines, polygons) with attributes - soil-sample sites, field boundaries. Raster = a grid of equal cells, each holding a value - elevation, satellite NDVI. Vector for discrete things with edges; raster for continuous things that vary everywhere.
   </details>

2. **Why does `field.area` give a tiny number and a warning?**
   <details>
   <summary>Click to check your understanding</summary>
   The layer is in EPSG:4326, so the "area" is in square degrees, which is not a real unit. Convert to a projected CRS in meters (EPSG:32616 for Illinois) with `.to_crs()` first; then `.area` is in m².
   </details>

3. **What does a GeoDataFrame add to a regular DataFrame?**
   <details>
   <summary>Click to check your understanding</summary>
   A `geometry` column (points/lines/polygons), a CRS that says what the coordinates mean, and spatial methods: `.plot()`, `.to_crs()`, `.area`, `.distance()`, `.buffer()`. All pandas methods still work.
   </details>

4. **What does the `extent=` argument do in `plt.imshow()`?**
   <details>
   <summary>Click to check your understanding</summary>
   It tells matplotlib the real-world coordinates of the image corners, so the raster is drawn as a map (in lon/lat) instead of as pixels (row/column numbers). Without it, vector layers won't line up on top.
   </details>

5. **Why did the residual map matter?**
   <details>
   <summary>Click to check your understanding</summary>
   The residuals clustered in space - nearby sites had similar errors. That violates the "independent errors" assumption from Module 02. The map made visible a problem the scatter plot could not show, and it motivates the spatial methods in Modules 03-04.
   </details>

### Can you do...?

1. **Build a GeoDataFrame from a table of lon/lat and plot it colored by an attribute?**
   ```python
   gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
   gdf.plot(column="value", legend=True)
   ```

2. **Compute the area of a polygon in acres?**
   ```python
   gdf.to_crs("EPSG:32616").area / 4046.86
   ```

3. **Open a GeoTIFF, print its CRS and bounds, and draw it with a polygon on top?**
   ```python
   with rasterio.open("elevation.tif") as src:
       fig, ax = plt.subplots()
       show(src, ax=ax)
       field.plot(ax=ax, facecolor="none", edgecolor="white")
   ```

4. **Extract raster values at point locations?**
   ```python
   coords = list(zip(gdf.geometry.x, gdf.geometry.y))
   with rasterio.open("elevation.tif") as src:
       gdf["elev"] = [v[0] for v in src.sample(coords)]
   ```

### Self-Check Exercises

- [ ] Complete Practice Exercises 1-4 above in your own Colab notebook
- [ ] Run the raster and vector examples in `Spatial_Plotting_python.ipynb` and change the colormaps
- [ ] Load one shapefile or GeoJSON of your own choosing and print its `.crs`

### Ready for Next Module?

Check off each item:

- [ ] I can explain vector vs raster and give an example of each
- [ ] I can build a GeoDataFrame from lon/lat columns and plot it
- [ ] I can create a polygon and overlay it with points
- [ ] I check `.crs` before overlaying or measuring, and convert to meters when I measure
- [ ] I can load a real vector file and make a choropleth
- [ ] I can create, save, open and plot a raster with rasterio
- [ ] I can extract raster values at points and run a regression on them

**If you checked all items**: You're ready for [Module 03: Geospatial Fundamentals](Module_03_Geospatial_Fundamentals.md), where CRS, sampling and interpolation go deeper.

**If you're unsure about some items**: Redo the section in a fresh Colab notebook, typing the code rather than pasting it. The CRS ideas in particular take a couple of passes.

---

## Common Mistakes to Avoid

1. **Measuring in degrees**
   `field.area` or `pts.buffer(150)` in EPSG:4326 gives nonsense. Convert with `.to_crs("EPSG:32616")` first.

2. **Overlaying layers with different CRS**
   They will silently draw in the wrong place or not appear at all. Print `.crs` of every layer (and `src.crs` for rasters) before plotting together.

3. **Forgetting `ax=ax`**
   Each `.plot()` without `ax=` opens a **new** figure, so layers never stack.

4. **Upside-down rasters**
   `imshow` puts row 0 at the top. Build the array north-first (as in Section 7) **or** pass `origin="lower"` - not both.

5. **Setting a CRS instead of converting**
   `.set_crs()` only **relabels** the numbers; `.to_crs()` actually **recalculates** them. Use `.set_crs()` only when a layer arrived with no CRS and you know what it should be.

6. **Skipping the install cell after a Colab restart**
   `rasterio` disappears when the runtime restarts. Re-run the first cell.

---

## Tips for Success

1. **Print the CRS first, every time**: `print(layer.crs)` before you do anything else. Make it a reflex.

2. **Draw one layer at a time**: If a map looks wrong, plot each layer alone. The one that's empty or in the wrong place is the culprit.

3. **Keep the field example**: `pts`, `field` and `elevation.tif` reappear in Module 03. Save the notebook.

4. **Map the residuals of every regression you fit from now on**: If they cluster, you have spatial structure - and a reason to keep reading.

5. **Type, don't paste**: Same advice as Module 01. Spatial code has many small arguments (`ax=`, `column=`, `crs=`), and typing them is how they stick.

---

## Next Steps

Ready for the full spatial toolkit?

→ **Continue to [Module 03: Geospatial Fundamentals](Module_03_Geospatial_Fundamentals.md)**

You'll learn:
- Coordinate reference systems in depth (UTM zones, State Plane, Web Mercator)
- Spatial sampling strategies
- Interpolation: filling the gaps between sample points with IDW and Kriging
- Overlay operations: zonal statistics of a raster inside polygons

---

*A map is the first diagnostic plot of spatial statistics. If you can see the pattern, you can model it.*
