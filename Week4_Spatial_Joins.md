# Week 4: Spatial Operations

**Difficulty**: ⭐⭐ Intermediate
**Time Estimate**: 2-3 hours
**Prerequisites**: Week 2 (regression basics), Module 03 (spatial data, CRS)

---

## Module Overview

**Spatial operations** combine or transform map layers using location. They come in two families:

| Family | Operations | What you get back |
|---|---|---|
| Geometry operations | buffer, union, dissolve, intersection, difference, clip | new shapes |
| Spatial joins | sjoin with within / contains / intersects / nearest | new attributes |

This is the everyday workhorse of spatial analysis. Real data never arrives in one tidy table - it arrives as separate layers that only share a location, and these operations are how you put them together.

All examples this week run on one real dataset, and every code block shows the output it actually produced.

### What You'll Learn
- Plot vector layers and check their CRS before any operation
- The geometry toolbox: `buffer`, `union`, `dissolve`, `intersection`, `difference`, `clip`
- Spatial joins: match rows by location with `sjoin` and its predicates
- Aggregate joined points (mean per polygon) and map the result

---

## Core Concepts

### 1. The Example Data

A real on-farm experiment (the DIFM project). A farmer varied seed rate and nitrogen rate on-the-go; at harvest the yield monitor recorded yield every second. Two layers, no shared ID column - only location:

| Layer | Type | What it holds |
|---|---|---|
| `TrialDesign.gpkg` | 4,283 polygons | the trial plots, each with its `SeedRate` and `NitrogenRate` |
| `Yield.gpkg` | 177,495 points | yield monitor readings (`Yld_Vol_Dr`, dry bu/ac) |

```python
import geopandas as gpd

plots = gpd.read_file("TrialDesign.gpkg").to_crs(32616)      # UTM 16N, meters
yield_pts = gpd.read_file("Yield.gpkg").to_crs(32616)
yield_pts = yield_pts[(yield_pts["Yld_Vol_Dr"] > 0) &
                      (yield_pts["Yld_Vol_Dr"] < 400)]       # drop bad readings

plots[["id", "SeedRate", "NitrogenRate", "geometry"]].head(3)
```

**Output:**

```
   id  SeedRate  NitrogenRate                                           geometry
0   1   36000.0     51.565325  POLYGON ((364853.6 4397604.451, 364853.687 439...
1   2   36000.0     51.565325  POLYGON ((364844.461 4397604.336, 364844.552 4...
2   3   36000.0     51.565325  POLYGON ((364839.177 4397609.665, 364844.552 4...
```

**One rule before any operation**: both layers must be in the **same CRS**, and for distances it should be a metric one (like UTM), not degrees.

```python
print(plots.crs)
print(yield_pts.crs == plots.crs)
```

**Output:**

```
EPSG:32616
True
```

#### The data at a glance

One line per layer is enough to see what you have:

```python
plots.plot(column="NitrogenRate", cmap="viridis", legend=True)
yield_pts.plot(column="Yld_Vol_Dr", cmap="RdYlGn", markersize=2, legend=True)
```

---

### 2. Buffer - Grow a Shape by a Distance

`buffer(d)` expands a geometry by `d` (in CRS units - meters here). Buffering a point makes a circle; buffering a line or polygon makes a corridor or a widened shape.

```python
field = plots.union_all()          # (union - explained next)
center = gpd.GeoSeries([field], crs=plots.crs).centroid.iloc[0]
print(center)

circle = center.buffer(120)        # a 120 m circle around the field center
print(round(circle.area, 1))       # area in m² - close to pi * 120²
```

**Output:**

```
POINT (364424.7239731141 4398008.071205432)
45166.3
```

**Real-world uses**: "all points within 100 m of a sensor", corridors around streams, exclusion zones around field edges.

---

### 3. Union and Dissolve - Merge Shapes

`union_all()` merges every geometry into one. `dissolve(by=...)` merges only the shapes that share a value - like `groupby` for geometry.

```python
field = plots.union_all()          # 4,283 plots -> one field outline
print(field.geom_type)
print(round(field.area / 10000, 1), "ha")
```

**Output:**

```
MultiPolygon
69.7 ha
```

```python
by_rate = plots.dissolve(by="NitrogenRate")   # one shape per N treatment
print(by_rate.shape)
print(list(by_rate.index.round(1)))
```

**Output:**

```
(6, 9)
[19.1, 27.5, 36.0, 44.5, 51.6, 61.5]
```

4,283 rows became 6 - one merged shape per nitrogen treatment.

#### Merging operations on the map

---

### 4. Intersection, Difference, Clip - Cut With Shapes

These take **two** layers and cut one with the other:

| Tool | What it does | GeoPandas |
|---|---|---|
| Intersection | keep only the area two layers share | `gpd.overlay(a, b, how="intersection")` |
| Difference | cut one layer's area out of another | `gpd.overlay(a, b, how="difference")` |
| Clip | cookie-cut any layer with a boundary | `gpd.clip(layer, boundary)` |

```python
circle_gdf = gpd.GeoDataFrame(geometry=[circle], crs=plots.crs)

# Intersection: which plot pieces are inside the circle?
pieces = gpd.overlay(plots, circle_gdf, how="intersection")
print(len(pieces), "plot pieces,", round(pieces.area.sum(), 1), "m² total")
```

**Output:**

```
310 plot pieces, 45166.3 m² total
```

The circle touches 310 plots, and the pieces add up to exactly the circle's area - nothing lost, nothing doubled.

```python
# Difference: the field with the circle cut out
hole = field.difference(circle)
print(round(field.area / 10000, 2), "->", round(hole.area / 10000, 2), "ha")

# Clip: only the yield points inside the circle
inside = gpd.clip(yield_pts, circle_gdf)
print(len(yield_pts), "->", len(inside), "points")
```

**Output:**

```
69.66 -> 65.14 ha
177494 -> 11263 points
```

#### Cutting operations on the map

---

### 5. Spatial Joins - Attach Attributes by Location

The operations above make new **shapes**. A spatial join instead attaches new **columns** - it is the spatial version of a table join.

**Attribute join** (what you know from pandas): match rows by a shared key column.

```python
merged = fields.merge(soil_tests, on="field_id")
```

**Spatial join**: match rows by where their geometries are. The geometry IS the key.

```python
joined = gpd.sjoin(points, polygons, predicate="within")
```

The `predicate` argument decides what "match" means:

| Predicate | Meaning | Typical use |
|---|---|---|
| `within` | left geometry is inside the right one | points into polygons |
| `contains` | left geometry contains the right one | polygons over points |
| `intersects` | they share any space at all | overlapping polygons |
| `nearest` | closest feature (via `sjoin_nearest`) | point to nearest road/station |

**Watch the vocabulary**: `intersects` (a predicate) asks a yes/no question for a join; `intersection` (an overlay) builds the shared shape. Same word family, different jobs.

---

### 6. Putting It All Together: Assembling the Trial Dataset

**The question**: what was the yield in each treatment plot? Every yield point must learn which plot it fell in - a spatial join, followed by an aggregation.

#### Step 1 - Look before you join

Plot both layers together first. If they don't overlap on the map, no predicate will save you.

#### Step 2 - The spatial join

```python
joined = gpd.sjoin(
    yield_pts[["Yld_Vol_Dr", "geometry"]],  # left: the points
    plots,                                   # right: the polygons
    predicate="within"                       # match rule
)
print(len(joined))
joined[["Yld_Vol_Dr", "index_right", "SeedRate", "NitrogenRate"]].head(3)
```

**Output:**

```
177457
   Yld_Vol_Dr  index_right  SeedRate  NitrogenRate
0    101.3887          287   36000.0     51.565325
1    110.8887          287   36000.0     51.565325
2     64.9492          287   36000.0     51.565325
```

Each yield point now carries the columns of the plot it fell in, plus `index_right` - the row number of that plot. The 37 points that fell outside every plot were dropped.

#### Step 3 - Aggregate: one number per plot

177 thousand points is too many - we want one yield value per plot. Group by the plot index, take the mean, attach it back to the polygons:

```python
plot_means = joined.groupby("index_right")["Yld_Vol_Dr"].mean()
print(plot_means.head(3))

plots["mean_yield"] = plot_means       # aligns by index automatically
plots[["NitrogenRate", "mean_yield"]].head(3)
```

**Output:**

```
index_right
0    171.470437
1    132.876781
2    185.042074
Name: Yld_Vol_Dr, dtype: float64

   NitrogenRate  mean_yield
0     51.565325  171.470437
1     51.565325  132.876781
2     51.565325  185.042074
```

```python
plots.plot(column="mean_yield", cmap="RdYlGn", legend=True)
```

#### Step 4 - The payoff

The joined table finally connects **treatment** (from the polygons) to **response** (from the points). Now ordinary statistics can take over:

```python
response = joined.groupby("index_right").agg(
    yld=("Yld_Vol_Dr", "mean"),
    N=("NitrogenRate", "first"))
response.boxplot(column="yld", by="N")
```

Every regression, ANOVA, and spatial model you fit later in this course starts from a table assembled exactly this way.

---

### 7. Common Mistakes to Avoid

1. **Different CRS on the two layers** - the #1 cause of "my join returned nothing". Check `crs` first, every time.
2. **Working in degrees**: in EPSG:4326, `buffer(100)` means 100 degrees, not 100 meters. Reproject to a metric CRS (like UTM) before any distance-based operation.
3. **Forgetting that unmatched points vanish**: `sjoin` is an inner join by default. Use `how="left"` to keep unmatched rows and see what fell outside.
4. **Duplicated rows with `intersects`**: a point on a shared plot boundary can match two polygons. If counts matter, check for duplicates after the join.

---

## Course Materials

**This week's data** (from the DIFM dataset-assembly case study):
- `TrialDesign.gpkg` and `Yield.gpkg` - ask your TA for a copy

**Reference**:
- Richard E. Plant (2019), **Spatial Data Analysis in Ecology and Agriculture Using R**, 2nd ed., CRC Press - the chapters on preparing and assembling spatial data cover this same workflow
- GeoPandas user guide: **Merging data** (`sjoin`, `sjoin_nearest`) and **Set operations with overlay**

---

## Study Checkpoints

### Can you explain...?
- [ ] The two families of spatial operations - new shapes vs new attributes
- [ ] What `buffer(120)` returns, and why the CRS units matter
- [ ] The difference between `union_all()` and `dissolve(by=...)`
- [ ] The difference between `intersects` (predicate) and `intersection` (overlay)
- [ ] Why we aggregate after joining points to plots

### Can you do...?
- [ ] Plot a vector layer colored by one of its columns
- [ ] Buffer a geometry, clip points to it, and dissolve polygons by a column
- [ ] Join a point layer to a polygon layer with `gpd.sjoin`
- [ ] Compute the mean of a point attribute per polygon and map it
