# Module 04: Spatial Statistics
## Spatial Autocorrelation, Semivariograms & Neighborhood Structures

**Difficulty**: ⭐⭐⭐⭐ Advanced
**Time Estimate**: 10-12 hours
**Prerequisites**: Module 03 (Geospatial fundamentals, basic Kriging)

---

## Module Overview

In Module 03, you learned to USE variograms for Kriging. Now you'll learn the theory BEHIND spatial statistics - why nearby things are related, how to measure that relationship, and how to model spatial patterns from first principles.

### What You'll Learn
- Deep understanding of spatial autocorrelation
- Building semivariograms from scratch
- Different variogram models and when to use them
- Neighborhood structures (Rook vs Queen contiguity)
- Spatial correlograms
- Distance measures for spatial analysis

### Why This Matters
Understanding spatial statistics at this level lets you:
- Diagnose problems in spatial models
- Choose appropriate methods for your data
- Understand assumptions and limitations
- Build custom spatial models

---

## Learning Objectives

By the end of this module, you will be able to:
- [ ] Calculate empirical semivariograms from scratch
- [ ] Fit and compare different variogram models
- [ ] Measure and interpret spatial autocorrelation
- [ ] Build contiguity matrices (Rook and Queen)
- [ ] Create and interpret spatial correlograms
- [ ] Choose appropriate distance metrics
- [ ] Understand lagged spatial correlation

---

## Core Concepts

### 1. Spatial Autocorrelation - The Foundation

**Tobler's First Law of Geography**: "Everything is related to everything else, but near things are more related than distant things."

**Simple explanation**: Values at nearby locations tend to be similar. Temperature 1 meter away is probably similar to here. Temperature 100 km away? Could be very different.

**Why it happens**:
- **Continuous processes**: Temperature, soil properties spread smoothly across space
- **Spillover effects**: Fertilizer applied here affects nearby plants
- **Common causes**: Nearby areas experience same weather, same soil parent material

**Positive spatial autocorrelation** (most common):
- High values cluster near high values
- Low values cluster near low values
- Example: Fertile areas of a field tend to cluster together

**Negative spatial autocorrelation** (rare):
- High values next to low values
- Checkerboard pattern
- Example: Competition (tall plants surrounded by stunted plants)

**How to measure**: Semivariograms and correlograms!

---

### 2. Semivariograms from Scratch

In Module 03, you used semivariograms for Kriging. Now let's build one from the ground up.

**The formula**:
```
γ(h) = (1 / 2N(h)) × Σ[z(xᵢ) - z(xᵢ + h)]²
```

**Step-by-step process**:

**Step 1**: Calculate all pairwise distances
```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Sample locations (x, y)
coords = np.array([
    [0, 0],
    [1, 0],
    [2, 0],
    [0, 1],
    [1, 1],
])

# Calculate all pairwise distances
distances = squareform(pdist(coords))
```

**Step 2**: Group distances into bins (lags)
```python
# Create distance bins (lags)
lag_bins = np.arange(0, 3, 0.5)  # Bins: 0-0.5, 0.5-1, 1-1.5, etc.
```

**Step 3**: For each bin, calculate semivariance
```python
values = np.array([45, 47, 50, 46, 49])  # Measured values at each location

def calculate_semivariogram(coords, values, lag_bins):
    distances = squareform(pdist(coords))
    n_lags = len(lag_bins) - 1

    lags = []
    gamma = []

    for i in range(n_lags):
        # Find pairs in this distance bin
        mask = (distances >= lag_bins[i]) & (distances < lag_bins[i+1])
        pairs = np.where(mask)

        if len(pairs[0]) > 0:
            # Calculate semivariance for these pairs
            diffs_squared = [(values[i] - values[j])**2
                             for i, j in zip(pairs[0], pairs[1])]
            gamma_h = np.mean(diffs_squared) / 2

            lags.append((lag_bins[i] + lag_bins[i+1]) / 2)
            gamma.append(gamma_h)

    return np.array(lags), np.array(gamma)

lags, gamma = calculate_semivariogram(coords, values, lag_bins)
```

**Step 4**: Plot empirical variogram
```python
import matplotlib.pyplot as plt

plt.scatter(lags, gamma)
plt.xlabel('Distance (lag)')
plt.ylabel('Semivariance γ(h)')
plt.title('Empirical Semivariogram')
plt.show()
```

**What you see**:
- At small distances: Low semivariance (nearby points are similar)
- At larger distances: Higher semivariance (distant points more different)
- Eventually plateaus at the sill (maximum variance)

---

### 3. Variogram Models - Choosing the Right One

You need to fit a mathematical model to your empirical variogram. Common choices:

#### Spherical Model (Most Common)
```
γ(h) = nugget + (sill - nugget) × [1.5(h/range) - 0.5(h/range)³]   for h < range
γ(h) = sill                                                          for h ≥ range
```

**When to use**: Moderate continuity, reaches sill at a definite distance
**Best for**: Soil properties, crop yields

**Shape**: Gradual rise, then levels off sharply at range

#### Exponential Model
```
γ(h) = nugget + (sill - nugget) × [1 - exp(-3h/range)]
```

**When to use**: Gradual spatial correlation decay
**Best for**: Atmospheric phenomena, temperature

**Shape**: Smooth exponential approach to sill (never quite reaches it)

#### Gaussian Model
```
γ(h) = nugget + (sill - nugget) × [1 - exp(-3h²/range²)]
```

**When to use**: Very smooth, continuous phenomena
**Best for**: Highly continuous processes

**Shape**: Very gradual start, then rapid increase

**How to choose**:
1. Plot empirical variogram
2. Try each model
3. Compare fits visually
4. Use cross-validation to test predictions

```python
from sklearn.model_selection import cross_val_score

# Fit different models and compare
models = ['spherical', 'exponential', 'gaussian']
for model in models:
    OK = OrdinaryKriging(x, y, values, variogram_model=model)
    # Evaluate prediction accuracy
```

---

### 4. Rook vs Queen Contiguity

**Contiguity**: Which locations are "neighbors"?

**Think of chess pieces**:

**Rook contiguity**: Neighbors share an edge
```
    [ ] [X] [ ]
    [X] [●] [X]    ● = focal cell
    [ ] [X] [ ]    X = neighbors (4 total)
```

**Queen contiguity**: Neighbors share edge OR corner
```
    [X] [X] [X]
    [X] [●] [X]    ● = focal cell
    [X] [X] [X]    X = neighbors (8 total)
```

**When it matters**:
- Analyzing raster data
- Spatial autoregressive models
- Detecting clusters
- Smoothing operations

**Example**: Detecting hot spots in yield data
- Rook: Stricter definition of "nearby"
- Queen: More inclusive, accounts for diagonal patterns

**In Python** (for raster):
```python
import numpy as np

def get_rook_neighbors(grid, i, j):
    """Get Rook neighbors of cell (i,j)"""
    neighbors = []
    rows, cols = grid.shape

    # Up, Down, Left, Right
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            neighbors.append((ni, nj))

    return neighbors

def get_queen_neighbors(grid, i, j):
    """Get Queen neighbors of cell (i,j)"""
    neighbors = []
    rows, cols = grid.shape

    # All 8 directions
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbors.append((ni, nj))

    return neighbors
```

---

### 5. Spatial Correlograms

**What it is**: Shows correlation at different distance lags (similar to variogram but uses correlation instead of variance).

**Simple explanation**: A variogram shows how different points become with distance. A correlogram shows how correlated they remain with distance.

**The pattern**:
- Lag 0: Correlation = 1 (perfect correlation with itself)
- Increasing lag: Correlation decreases
- Large lag: Correlation ≈ 0 (no relationship)

**Creating a correlogram**:
```python
def spatial_correlogram(coords, values, max_lag, n_bins):
    from scipy.spatial.distance import pdist, squareform
    from scipy.stats import pearsonr

    distances = squareform(pdist(coords))
    lag_bins = np.linspace(0, max_lag, n_bins+1)

    lags = []
    correlations = []

    for i in range(n_bins):
        mask = (distances >= lag_bins[i]) & (distances < lag_bins[i+1])
        pairs = np.where(mask)

        if len(pairs[0]) > 10:  # Need enough pairs
            values_i = values[pairs[0]]
            values_j = values[pairs[1]]
            corr, _ = pearsonr(values_i, values_j)

            lags.append((lag_bins[i] + lag_bins[i+1]) / 2)
            correlations.append(corr)

    return np.array(lags), np.array(correlations)

# Plot
lags, corrs = spatial_correlogram(coords, values, max_lag=10, n_bins=20)
plt.plot(lags, corrs, 'o-')
plt.axhline(0, color='k', linestyle='--')
plt.xlabel('Distance lag')
plt.ylabel('Correlation')
plt.title('Spatial Correlogram')
plt.show()
```

**Interpreting**:
- High correlation at small lags: Strong spatial autocorrelation
- Correlation drops to zero quickly: Short-range dependence
- Correlation remains high: Long-range dependence

**Variogram vs Correlogram**:
- Variogram: Emphasizes differences (variance)
- Correlogram: Emphasizes similarity (correlation)
- They're inverse relationships: high correlation = low semivariance

---

### 6. Distance Measures

Not all distances are created equal!

#### Euclidean Distance (Most Common)
```
d = √[(x₁ - x₂)² + (y₁ - y₂)²]
```
**Use**: Standard distance, works for most applications

#### Manhattan Distance
```
d = |x₁ - x₂| + |y₁ - y₂|
```
**Use**: When movement is constrained to grid (city blocks)

#### Great Circle Distance
```
(Complex formula using haversine)
```
**Use**: Distance on Earth's surface (lat/lon coordinates)
**Important**: Accounts for Earth's curvature

```python
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """Great circle distance between two lat/lon points (km)"""
    R = 6371  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1, lat2 = radians(lat1), radians(lat2)

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c
```

**When it matters**: Large geographic areas where Earth's curvature is significant (>100 km)

---

## Course Materials

### Primary Notebooks

1. **[python_notebooks/ModelingSpatialVariability_Part1.ipynb](/tmp/cpsc444-study/python_notebooks/ModelingSpatialVariability_Part1.ipynb)**
   - Building semivariograms from scratch
   - Understanding semivariance calculation
   - Empirical variogram construction

2. **[python_notebooks/ModelingSpatialVariability-Part2.ipynb](/tmp/cpsc444-study/python_notebooks/ModelingSpatialVariability-Part2.ipynb)**
   - Advanced variogram modeling
   - Fitting different models
   - Model comparison

3. **[python_notebooks/ModelingSpatialVariability_Part3.ipynb](/tmp/cpsc444-study/python_notebooks/ModelingSpatialVariability_Part3.ipynb)**
   - Applications of spatial variability models
   - Real-world examples

4. **[python_notebooks/DistanceMeasures.ipynb](/tmp/cpsc444-study/python_notebooks/DistanceMeasures.ipynb)**
   - Different distance metrics
   - When to use each
   - Impact on spatial analysis

5. **[python_notebooks/ToyRaster_Contiguity.ipynb](/tmp/cpsc444-study/python_notebooks/ToyRaster_Contiguity.ipynb)**
   - Rook vs Queen contiguity
   - Building neighborhood matrices
   - Applications in raster analysis

6. **[python_notebooks/ToyRaster_Contiguity_Extended_pub.ipynb](/tmp/cpsc444-study/python_notebooks/ToyRaster_Contiguity_Extended_pub.ipynb)**
   - Extended contiguity analysis
   - Advanced neighborhood structures

7. **[python_notebooks/PairsPlot_Correlogram.ipynb](/tmp/cpsc444-study/python_notebooks/PairsPlot_Correlogram.ipynb)**
   - Creating spatial correlograms
   - Interpreting lagged correlation
   - Comparing to variograms

---

## Study Checkpoints

### Can you explain...?

1. **What is spatial autocorrelation and why does it occur?**
2. **How is a semivariogram different from a correlogram?**
3. **What do nugget, sill, and range represent physically?**
4. **When would you use Rook vs Queen contiguity?**
5. **Why might you choose an exponential over a spherical variogram model?**

### Can you do...?

1. **Calculate an empirical semivariogram from scratch (without pykrige)?**
2. **Fit different variogram models and compare them?**
3. **Build a contiguity matrix for a raster?**
4. **Create and interpret a spatial correlogram?**
5. **Choose the appropriate distance metric for your data?**

### Ready for Next Module?

- [ ] I can build semivariograms from raw data
- [ ] I understand different variogram models
- [ ] I know Rook vs Queen contiguity
- [ ] I can create correlograms
- [ ] I understand spatial autocorrelation deeply

**Ready?** → [Module 05: Advanced Regression](Module_05_Advanced_Regression.md)

---

*Spatial statistics is the foundation of all spatial analysis. Master these concepts and you'll understand what's really happening in spatial models!*
