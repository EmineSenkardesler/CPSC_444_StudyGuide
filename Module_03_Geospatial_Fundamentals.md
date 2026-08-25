# Module 03: Geospatial Fundamentals
## Spatial Data, Coordinate Systems & Interpolation

**Difficulty**: ⭐⭐⭐ Intermediate
**Time Estimate**: 8-10 hours
**Prerequisites**: Modules 01 (Python basics), 02 (Statistics & regression)

---

## Module Overview

Until now, you've worked with regular data - numbers in tables. But what if your data has a LOCATION component? That's spatial data! A temperature reading isn't just "75°F" - it's "75°F at GPS coordinates (40.11, -88.21)." This module teaches you how to work with, visualize, and analyze data that exists in geographic space.

### What You'll Learn
- What makes spatial data different
- Raster data (like satellite images) vs vector data (like points/polygons)
- Coordinate reference systems (how locations are represented)
- How to fill gaps in spatial data (interpolation with Kriging and IDW)
- Spatial sampling strategies
- How to create and manipulate spatial data files

### Why This Matters
Almost everything in agriculture, environmental science, and earth sciences has a spatial component:
- Soil samples from different parts of a field
- Weather measurements from different stations
- Satellite images showing crop health
- Field boundaries and management zones

Understanding spatial data is essential for working with real-world agricultural and environmental datasets.

---

## Learning Objectives

By the end of this module, you will be able to:
- [ ] Distinguish between raster and vector data formats
- [ ] Load and visualize spatial data in Python
- [ ] Understand and transform coordinate reference systems
- [ ] Perform spatial sampling
- [ ] Use Kriging to interpolate spatial data
- [ ] Create shapefiles and GeoTIFFs
- [ ] Overlay and combine spatial datasets

---

## Core Concepts

### 1. What is Spatial Data?

**Simple explanation**: Data where each observation has a location (coordinates) attached to it.

**Regular data**:
```
Temperature
-----------
75°F
72°F
80°F
```

**Spatial data**:
```
Latitude  Longitude  Temperature
----------------------------------------
40.10     -88.20     75°F
40.15     -88.25     72°F
40.08     -88.18     80°F
```

**What makes it special**:
1. **Nearby things are related**: Soil samples 10 feet apart are more similar than samples 1 mile apart
2. **Location matters**: The value at (40.10, -88.20) can influence neighbors
3. **Spatial patterns exist**: Hot spots, cold spots, gradients, clusters

**Real-world example**: Measuring corn yield across a field. Yields aren't random - high-yielding areas tend to cluster together (maybe better soil there), and low-yielding areas cluster too (maybe poor drainage). This spatial structure is what we analyze!

---

### 2. Raster vs Vector Data

Think of this like the difference between a photo and a drawing:

#### Raster Data (Like a Photo)

**What it is**: Space is divided into a grid of cells (pixels), each with a value.

**Example**: Satellite image - each pixel (say, 30m × 30m) has a value like:
- Vegetation index (how green it is)
- Temperature
- Elevation

**Visual representation**:
```
Grid of cells, each with a value:
[45] [47] [46] [48]
[44] [46] [47] [49]
[46] [45] [48] [47]
```

**Common uses**:
- Satellite imagery
- Elevation maps (DEMs - Digital Elevation Models)
- Temperature maps
- Rainfall maps

**File formats**: GeoTIFF (.tif), IMG, HDF

**Advantages**:
- Great for continuous data (temperature, elevation)
- Easy to do map algebra (add, subtract rasters)
- Satellite/drone imagery is naturally raster

**Disadvantages**:
- File sizes can be huge
- Fixed resolution (can't zoom in infinitely)

#### Vector Data (Like a Drawing)

**What it is**: Features defined by coordinates - points, lines, or polygons.

**Types**:
1. **Points**: Single locations (weather stations, sample points)
2. **Lines**: Connected points (roads, rivers, field borders)
3. **Polygons**: Closed shapes (field boundaries, counties, management zones)

**Example - Field boundary (polygon)**:
```
Points defining a field:
(40.100, -88.200)
(40.100, -88.210)
(40.110, -88.210)
(40.110, -88.200)
[connects back to first point]
```

**Common uses**:
- Field boundaries
- Sample point locations
- Roads and rivers
- Administrative boundaries

**File formats**: Shapefile (.shp + .shx + .dbf), GeoPackage (.gpkg), GeoJSON

**Advantages**:
- Precise boundaries
- Small file sizes
- Can zoom in infinitely
- Easy to attach attributes (field ID, crop type, etc.)

**Disadvantages**:
- Not ideal for continuous phenomena (like temperature)
- Complex operations can be slow

**When to use each**:
- Raster: Continuous data (temperature, elevation, imagery)
- Vector: Discrete features (field boundaries, sample points)

---

### 3. Coordinate Reference Systems (CRS)

**The problem**: Earth is a 3D sphere, but maps are 2D. How do we represent locations?

**What is a CRS?**: A system for defining where things are on Earth.

#### Two Main Types:

**1. Geographic CRS (Latitude/Longitude)**

- Uses degrees: latitude (N/S), longitude (E/W)
- Example: (40.1106°N, 88.2073°W)
- **Advantage**: Universal, everyone understands it
- **Disadvantage**: Distances aren't equal everywhere (1° longitude in Alaska is shorter than 1° at the equator)

**Most common**: WGS84 (EPSG:4326) - what GPS uses

**2. Projected CRS (X/Y in meters)**

- Uses meters (or feet) from a reference point
- Example: (500000 m East, 4430000 m North)
- **Advantage**: Distances and areas are accurate, easy to measure
- **Disadvantage**: Only accurate in a specific region

**Common projected systems**:
- UTM (Universal Transverse Mercator): divides world into zones
- State Plane (USA): optimized for each state
- Web Mercator (EPSG:3857): what Google Maps uses

#### Why CRS Matters

**Problem**: You have a field boundary in one CRS and satellite imagery in another. If you don't align them, they won't overlay correctly!

**Solution**: Transform everything to the same CRS before analysis.

**Example in Python**:
```python
import geopandas as gpd

# Load shapefile (might be in one CRS)
fields = gpd.read_file('fields.shp')
print(fields.crs)  # Check current CRS

# Transform to different CRS (e.g., UTM Zone 16N)
fields_utm = fields.to_crs('EPSG:32616')

# Now distances and areas are in meters!
fields_utm['area_m2'] = fields_utm.geometry.area
fields_utm['area_acres'] = fields_utm['area_m2'] / 4047
```

**Rule of thumb**:
- Use geographic CRS (lat/lon) for global data or display
- Use projected CRS (meters) for analysis, area calculations, distance measurements

---

### 4. Spatial Interpolation - The Big Picture

**The problem**: You measured soil nutrients at 50 points in a field. What about the other 99% of the field where you didn't sample?

**Solution**: Interpolation - estimating values at unsampled locations based on nearby sampled points.

**Simple analogy**: You know it's 70°F in City A and 80°F in City B (50 miles apart). What's the temperature halfway between? Probably around 75°F. That's interpolation!

#### Two Common Methods:

**1. IDW (Inverse Distance Weighting)**
- **Idea**: Nearby points have more influence than distant points
- **Simple**: Average of neighbors, weighted by distance
- **Fast**: But assumes smooth gradients

**2. Kriging (More sophisticated)**
- **Idea**: Use spatial correlation structure to make best predictions
- **Better**: Accounts for how similarity changes with distance
- **Slower**: But gives you prediction uncertainty too

We'll focus on Kriging since it's more powerful for agricultural/environmental data.

---

### 5. Kriging Interpolation

**What it is**: A sophisticated interpolation method that uses the spatial correlation structure in your data to predict values at unsampled locations.

**Simple explanation**: Kriging looks at how similar values are at different distances, then uses that pattern to make predictions. It also tells you how confident to be in each prediction!

#### The Process:

**Step 1: Calculate the empirical variogram**

**What**: A graph showing how different points become as distance increases.

**Simple analogy**: Measure temperature at pairs of points:
- Points 1 meter apart differ by 0.5°C on average
- Points 10 meters apart differ by 2°C
- Points 100 meters apart differ by 5°C

As distance increases, points become more different (less correlated).

**Formula** (don't panic!):
```
γ(h) = (1/2N(h)) × Σ(z_i - z_j)²
```

**In words**:
- For all pairs of points that are distance h apart
- Calculate how different they are: (value_i - value_j)²
- Average those differences
- Divide by 2

**What you get**: A curve showing variance vs distance

**Step 2: Fit a model to the variogram**

**Common models**:

1. **Spherical**: Gradual increase, then levels off
   ```
   γ(h) = nugget + sill × [1.5(h/range) - 0.5(h/range)³]  for h < range
   γ(h) = nugget + sill                                     for h ≥ range
   ```

2. **Exponential**: Smooth exponential curve
   ```
   γ(h) = nugget + sill × [1 - exp(-3h/range)]
   ```

3. **Gaussian**: Very smooth, for very continuous data
   ```
   γ(h) = nugget + sill × [1 - exp(-3h²/range²)]
   ```

**Three key parameters**:

1. **Nugget**: Variance at distance = 0 (measurement error + very small-scale variation)
2. **Sill**: Maximum variance (plateau value)
3. **Range**: Distance at which points become uncorrelated

**Simple visualization**:
```
Semivariance
    |
    |  ....... ←─── Sill (max variance)
    |  /
    | /        ←─── Range (distance to sill)
    |/
    *──────────────> Distance
    ↑
  Nugget
```

**Step 3: Use the model to make predictions (Ordinary Kriging)**

For each unsampled location:
1. Find nearby sampled points
2. Weight them based on distance AND spatial correlation structure
3. Compute weighted average = prediction
4. Also compute prediction variance = uncertainty

**Why Kriging is better than simple averaging**:
- Accounts for spatial structure (not just distance)
- Gives you uncertainty estimates
- Minimizes prediction error

#### Kriging in Python:

```python
from pykrige.ok import OrdinaryKriging
import numpy as np

# Sample data: (x, y, value)
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 2, 1, 0])
values = np.array([45, 47, 50, 46, 44])  # e.g., nitrogen levels

# Create Kriging model
OK = OrdinaryKriging(
    x, y, values,
    variogram_model='spherical',
    verbose=False,
    enable_plotting=False
)

# Predict on a grid
grid_x = np.arange(0, 4, 0.1)
grid_y = np.arange(0, 2, 0.1)
z_pred, ss_pred = OK.execute('grid', grid_x, grid_y)

# z_pred = predicted values
# ss_pred = prediction variance (uncertainty)
```

**Output**:
- Predicted value at every grid point
- Uncertainty at every grid point (higher where samples are sparse)

---

### 6. Spatial Sampling Strategies

**The problem**: You can't measure everywhere. Where should you take samples?

#### Common Strategies:

**1. Random Sampling**
- **Idea**: Place samples randomly across the area
- **Advantage**: Unbiased, good for statistical inference
- **Disadvantage**: Might miss important areas, might cluster by chance

**2. Systematic/Grid Sampling**
- **Idea**: Regular grid of samples
- **Advantage**: Even coverage, easy to plan
- **Disadvantage**: Might align with hidden patterns (e.g., field rows)

**3. Stratified Sampling**
- **Idea**: Divide area into zones (strata), sample within each
- **Advantage**: Ensures coverage of different conditions
- **Example**: Sample high, medium, low elevation areas separately

**4. Clustered Sampling**
- **Idea**: Multiple samples in selected locations
- **Advantage**: Good for understanding local variability
- **Use case**: Detailed study of specific problem areas

**For Kriging**: Regular grid or random sampling works well. Need enough samples to capture spatial structure (usually 50-100 minimum).

**In Python**:
```python
import numpy as np

# Random sampling within a field boundary
n_samples = 50
x_samples = np.random.uniform(0, 100, n_samples)  # Random x between 0-100
y_samples = np.random.uniform(0, 50, n_samples)   # Random y between 0-50

# Grid sampling
x_grid = np.linspace(0, 100, 10)  # 10 points from 0 to 100
y_grid = np.linspace(0, 50, 5)    # 5 points from 0 to 50
X, Y = np.meshgrid(x_grid, y_grid)  # Creates all combinations
```

---

### 7. Working with Spatial Data in Python

#### Loading Raster Data:

```python
import rasterio
import matplotlib.pyplot as plt

# Load a GeoTIFF
with rasterio.open('elevation.tif') as src:
    elevation = src.read(1)  # Read band 1
    print(f"CRS: {src.crs}")
    print(f"Shape: {elevation.shape}")
    print(f"Resolution: {src.res}")

    # Plot it
    plt.imshow(elevation, cmap='terrain')
    plt.colorbar(label='Elevation (m)')
    plt.title('Elevation Map')
    plt.show()
```

#### Loading Vector Data:

```python
import geopandas as gpd

# Load shapefile or GeoPackage
fields = gpd.read_file('fields.gpkg')

# Explore
print(fields.head())
print(fields.crs)

# Plot
fields.plot(column='yield', legend=True, cmap='YlGn')
plt.title('Yield by Field')
plt.show()
```

#### Creating a GeoTIFF from Interpolation:

```python
import rasterio
from rasterio.transform import from_origin
import numpy as np

# After Kriging, you have a grid of predictions: z_pred

# Define spatial reference
transform = from_origin(xmin, ymax, pixel_width, pixel_height)

# Write to GeoTIFF
with rasterio.open(
    'prediction.tif', 'w',
    driver='GTiff',
    height=z_pred.shape[0],
    width=z_pred.shape[1],
    count=1,
    dtype=z_pred.dtype,
    crs='EPSG:32616',  # UTM Zone 16N
    transform=transform,
) as dst:
    dst.write(z_pred, 1)
```

---

### 8. Spatial Overlay Operations

**What it is**: Combining multiple spatial layers to answer questions.

**Example question**: "What's the average yield for each soil type?"

**Process**:
1. Have a yield raster
2. Have a soil type polygon layer
3. Overlay them to extract yield values for each soil type

```python
import geopandas as gpd
import rasterstats

# Load soil polygons
soils = gpd.read_file('soil_types.shp')

# Extract statistics from yield raster for each soil polygon
stats = rasterstats.zonal_stats(
    soils,
    'yield.tif',
    stats=['mean', 'std', 'min', 'max']
)

# Add to GeoDataFrame
soils['mean_yield'] = [s['mean'] for s in stats]
soils['std_yield'] = [s['std'] for s in stats]

# Now you can analyze yield by soil type!
print(soils[['soil_type', 'mean_yield', 'std_yield']])
```

---

## Course Materials

### Primary Notebooks

1. **[w01-exercises/Spatial_Plotting_python.ipynb](/tmp/cpsc444-study/w01-exercises/Spatial_Plotting_python.ipynb)**
   - Loading and visualizing rasters with rasterio
   - Working with geopandas for vector data
   - Basic spatial plotting

2. **[w01-exercises/Spatial_sampling_functions.ipynb](/tmp/cpsc444-study/w01-exercises/Spatial_sampling_functions.ipynb)**
   - Different spatial sampling strategies
   - Random, grid, and stratified sampling
   - Evaluating sampling designs

3. **[w01-exercises/SamplingExamples.ipynb](/tmp/cpsc444-study/w01-exercises/SamplingExamples.ipynb)**
   - Practical sampling demonstrations
   - Comparing sampling methods
   - Sample size considerations

4. **[w01-exercises/Kriging-ECto30-python.ipynb](/tmp/cpsc444-study/w01-exercises/Kriging-ECto30-python.ipynb)**
   - Complete Kriging workflow
   - Empirical variogram calculation
   - Variogram model fitting (spherical, exponential)
   - Ordinary Kriging interpolation
   - Creating GeoTIFF output

5. **[w01-exercises/Geospatial_Overlay_Tutorial.ipynb](/tmp/cpsc444-study/w01-exercises/Geospatial_Overlay_Tutorial.ipynb)**
   - Overlaying vector and raster data
   - Spatial joins
   - Extracting values from rasters

6. **[w01-exercises/TrialDesign_SpatialMapping_Tutorial.ipynb](/tmp/cpsc444-study/w01-exercises/TrialDesign_SpatialMapping_Tutorial.ipynb)**
   - Field trial mapping
   - Creating spatial maps from trial data
   - Visualizing treatment effects spatially

---

## Key Formulas

### Semivariance
```
γ(h) = (1 / 2N(h)) × Σ [z(xᵢ) - z(xᵢ + h)]²
```
**In words**: For all pairs of points separated by distance h, calculate half the average squared difference.

### Spherical Variogram Model
```
γ(h) = nugget + (sill - nugget) × [1.5(h/range) - 0.5(h/range)³]   for h < range
γ(h) = sill                                                          for h ≥ range
```

### Kriging Prediction
```
ẑ(x₀) = Σ λᵢ × z(xᵢ)
```
**In words**: Predicted value = weighted sum of nearby observations, where weights (λ) are optimized based on spatial correlation.

### Kriging Variance (Uncertainty)
```
σ²(x₀) = γ(0) - Σ λᵢ × γ(xᵢ, x₀)
```
**In words**: Prediction uncertainty depends on how far the location is from sample points.

---

## Study Checkpoints

### Can you explain...?

1. **What's the difference between raster and vector data? When would you use each?**
   <details>
   <summary>Click to check</summary>
   Raster = grid of cells, each with a value. Good for continuous data (temperature, elevation, satellite imagery). Vector = points/lines/polygons defined by coordinates. Good for discrete features (boundaries, sample points). Use raster for imagery/continuous phenomena; vector for precise features.
   </details>

2. **Why do coordinate reference systems matter?**
   <details>
   <summary>Click to check</summary>
   Different datasets might use different CRS. If you don't align them (transform to same CRS), they won't overlay correctly. Also, geographic CRS (lat/lon) gives distorted distances/areas. Projected CRS (meters) is needed for accurate measurements.
   </details>

3. **What does a variogram tell you, and why is it important for Kriging?**
   <details>
   <summary>Click to check</summary>
   A variogram shows how similarity decreases with distance. It reveals the spatial correlation structure. Kriging uses this structure to weight nearby points optimally when making predictions. The nugget/sill/range parameters describe the pattern of spatial dependence.
   </details>

4. **How is Kriging different from simple averaging?**
   <details>
   <summary>Click to check</summary>
   Simple averaging treats all nearby points equally. Kriging weights points based on distance AND spatial correlation structure (from the variogram). Kriging also provides prediction uncertainty. Result: better predictions, especially when spatial patterns are complex.
   </details>

5. **What's the difference between nugget, sill, and range in a variogram?**
   <details>
   <summary>Click to check</summary>
   Nugget = variance at distance zero (measurement error + micro-scale variation). Sill = maximum variance (plateau value). Range = distance at which points become uncorrelated (where variogram reaches sill). These parameters describe spatial correlation structure.
   </details>

### Can you do...?

1. **Load a raster file and visualize it?**
   ```python
   # Use rasterio and matplotlib
   # Check Spatial_Plotting_python.ipynb
   ```

2. **Load a shapefile and check its CRS?**
   ```python
   import geopandas as gpd
   data = gpd.read_file('file.shp')
   print(data.crs)
   ```

3. **Transform a GeoDataFrame to a different CRS?**
   ```python
   data_utm = data.to_crs('EPSG:32616')
   ```

4. **Perform Kriging interpolation on sample points and create a prediction map?**
   ```python
   # Follow the workflow in Kriging-ECto30-python.ipynb
   # Calculate variogram, fit model, predict on grid
   ```

5. **Calculate the area of a polygon in a projected CRS?**
   ```python
   # First transform to projected CRS (meters)
   # Then: polygon.area gives area in m²
   ```

### Self-Check Exercises

Work through these notebooks:

- [ ] Load and plot rasters and vectors in `Spatial_Plotting_python.ipynb`
- [ ] Try different sampling strategies in `Spatial_sampling_functions.ipynb`
- [ ] Complete the full Kriging workflow in `Kriging-ECto30-python.ipynb`
- [ ] Practice overlay operations in `Geospatial_Overlay_Tutorial.ipynb`
- [ ] Understand field trial mapping in `TrialDesign_SpatialMapping_Tutorial.ipynb`

### Ready for Next Module?

Check off each item:

- [ ] I understand raster vs vector data
- [ ] I can load and visualize spatial data in Python
- [ ] I know what CRS is and why it matters
- [ ] I can transform between different CRS
- [ ] I understand how variograms work
- [ ] I can perform Kriging interpolation
- [ ] I know different spatial sampling strategies
- [ ] I can create GeoTIFFs and shapefiles

**All checked?** Move on to [Module 04: Spatial Statistics](Module_04_Spatial_Statistics.md)

**Need more practice?** Spend more time with the Kriging notebook. It's complex but crucial!

---

## Common Mistakes to Avoid

1. **Mixing CRS without transforming**
   - Always check CRS and transform to match before overlaying

2. **Using lat/lon for distance calculations**
   - Transform to projected CRS first, or distances will be wrong

3. **Not checking variogram fit**
   - Plot your empirical variogram and fitted model - make sure it fits well!

4. **Too few sample points for Kriging**
   - Need 50+ points to get reliable variogram, more is better

5. **Extrapolating too far**
   - Kriging predictions far from sample points are unreliable
   - Check prediction variance - high variance = low confidence

---

## Tips for Success

1. **Always visualize first**: Plot your data before analysis. Does the spatial pattern make sense?

2. **Check CRS immediately**: First thing - print and verify CRS of all datasets

3. **Understand your variogram**: Don't just fit it automatically. Look at the plot. Does the model fit well? Do the parameters make sense?

4. **Start with IDW**: Before Kriging, try simple IDW interpolation to get a baseline

5. **Validate predictions**: Hold out some sample points, predict them with Kriging, compare predicted vs actual

6. **Use domain knowledge**: Does your interpolated map make sense given what you know about the field/region?

---

## Next Steps

Ready for advanced spatial statistics?

→ **Continue to [Module 04: Spatial Statistics](Module_04_Spatial_Statistics.md)**

You'll learn:
- Spatial autocorrelation in depth
- Advanced semivariogram modeling
- Contiguity and neighborhood structures
- Spatial correlograms

---

*Spatial data is everywhere in environmental and agricultural sciences. Master these fundamentals and you'll be able to analyze any geographic dataset!*
