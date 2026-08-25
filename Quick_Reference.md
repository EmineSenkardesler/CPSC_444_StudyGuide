# Quick Reference Guide
## Formulas, Code Patterns & Library Usage

This is your cheat sheet for quick lookups while working through the modules or applying concepts to your own projects.

---

## Key Formulas

### Statistics Basics

**Mean**
```
μ = (Σxᵢ) / n
```

**Standard Deviation**
```
σ = √[(Σ(xᵢ - μ)²) / n]
```

**Variance**
```
σ² = (Σ(xᵢ - μ)²) / n
```

---

### Regression

**Simple Linear Regression**
```
y = β₀ + β₁x + ε
```

**Multiple Linear Regression**
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
```

**Normal Equation (Matrix Form)**
```
β = (XᵀX)⁻¹Xᵀy
```

**R-squared**
```
R² = 1 - (SS_residual / SS_total)
```

**Mean Squared Error**
```
MSE = (1/n) Σ(yᵢ - ŷᵢ)²
```

---

### Logistic Regression

**Sigmoid Function**
```
P(y=1) = 1 / (1 + e^(-z))
where z = β₀ + β₁x₁ + β₂x₂ + ...
```

---

### Spatial Statistics

**Semivariance**
```
γ(h) = (1 / 2N(h)) × Σ[z(xᵢ) - z(xᵢ + h)]²
```

**Spherical Variogram Model**
```
γ(h) = nugget + (sill - nugget) × [1.5(h/range) - 0.5(h/range)³]   for h < range
γ(h) = sill                                                          for h ≥ range
```

**Exponential Variogram Model**
```
γ(h) = nugget + (sill - nugget) × [1 - exp(-3h/range)]
```

**Intraclass Correlation**
```
ICC = σ²_between / (σ²_between + σ²_within)
```

---

### Regularization

**Ridge (L2)**
```
Minimize: Σ(y - ŷ)² + λΣβ²
```

**Lasso (L1)**
```
Minimize: Σ(y - ŷ)² + λΣ|β|
```

---

### Mixed Models

**Random Intercept**
```
y_ij = (β₀ + u_j) + β₁x_ij + ε_ij
where u_j ~ N(0, σ²_between)
```

**Random Slope**
```
y_ij = (β₀ + u_0j) + (β₁ + u_1j)x_ij + ε_ij
```

---

## Essential Python Code Patterns

### Data Loading & Manipulation

```python
import numpy as np
import pandas as pd

# Load CSV
data = pd.read_csv('file.csv')

# Basic stats
data.describe()
data['column'].mean()
data['column'].std()

# Select columns
X = data[['col1', 'col2', 'col3']]
y = data['target']

# Handle missing data
data.dropna()  # Remove rows with NaN
data.fillna(0)  # Fill NaN with 0
```

---

### Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plot
plt.scatter(x, y)
plt.xlabel('X label')
plt.ylabel('Y label')
plt.title('Title')
plt.show()

# Histogram
plt.hist(data, bins=20)

# Heatmap (correlation matrix)
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')

# Plotly (interactive)
import plotly.graph_objects as go
fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))
fig.show()
```

---

### Linear Regression

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# Fit model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# Coefficients
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")
```

---

### Logistic Regression

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score

# Fit
log_model = LogisticRegression()
log_model.fit(X_train, y_train)

# Predict classes
y_pred = log_model.predict(X_test)

# Predict probabilities
y_prob = log_model.predict_proba(X_test)[:, 1]

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)
```

---

### Train-Test Split & Cross-Validation

```python
from sklearn.model_selection import train_test_split, cross_val_score

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# K-fold cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"Mean R²: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

---

### Ridge & Lasso Regression

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import GridSearchCV

# Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

# Lasso
lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)

# Hyperparameter tuning
param_grid = {'alpha': [0.1, 1, 10, 100]}
grid_search = GridSearchCV(Ridge(), param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_alpha = grid_search.best_params_['alpha']
```

---

### Random Forest

```python
from sklearn.ensemble import RandomForestRegressor

# Fit
rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
rf.fit(X_train, y_train)

# Predict
y_pred = rf.predict(X_test)

# Feature importance
importances = rf.feature_importances_
feature_names = X.columns
for name, imp in zip(feature_names, importances):
    print(f"{name}: {imp:.3f}")
```

---

### XGBoost

```python
import xgboost as xgb

# Fit
xgb_model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
xgb_model.fit(X_train, y_train)

# Predict
y_pred = xgb_model.predict(X_test)

# Feature importance
importances = xgb_model.feature_importances_
```

---

### Spatial Data - Loading

```python
import geopandas as gpd
import rasterio

# Load vector data (shapefile, GeoPackage)
gdf = gpd.read_file('fields.shp')
print(gdf.crs)
gdf.plot()

# Load raster data (GeoTIFF)
with rasterio.open('elevation.tif') as src:
    raster = src.read(1)  # Read band 1
    print(f"CRS: {src.crs}")
    print(f"Shape: {raster.shape}")
```

---

### Spatial Data - CRS Transformation

```python
# Check CRS
print(gdf.crs)

# Transform to different CRS
gdf_utm = gdf.to_crs('EPSG:32616')  # UTM Zone 16N
gdf_wgs84 = gdf.to_crs('EPSG:4326')  # WGS84 (lat/lon)

# Calculate area (after transforming to projected CRS)
gdf_utm['area_m2'] = gdf_utm.geometry.area
gdf_utm['area_acres'] = gdf_utm['area_m2'] / 4047
```

---

### Kriging

```python
from pykrige.ok import OrdinaryKriging
import numpy as np

# Sample data
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 2, 1, 0])
values = np.array([45, 47, 50, 46, 44])

# Fit Kriging model
OK = OrdinaryKriging(
    x, y, values,
    variogram_model='spherical',
    verbose=False
)

# Predict on grid
grid_x = np.arange(0, 4, 0.1)
grid_y = np.arange(0, 2, 0.1)
z_pred, ss_pred = OK.execute('grid', grid_x, grid_y)
```

---

### Mixed Models

```python
import statsmodels.formula.api as smf

# Random intercept
model = smf.mixedlm(
    "yield ~ fertilizer + temperature",  # Fixed effects
    data,
    groups=data["field_id"]  # Random intercept
)
result = model.fit()
print(result.summary())

# Random slope
model = smf.mixedlm(
    "yield ~ fertilizer",
    data,
    groups=data["field_id"],
    re_formula="~fertilizer"  # Random slope
)
result = model.fit()
```

---

## Library Quick Reference

### When to Use Each Library

**Numpy**: Arrays, mathematical operations
```python
import numpy as np
arr = np.array([1, 2, 3])
mean = np.mean(arr)
```

**Pandas**: Tabular data, CSV files
```python
import pandas as pd
df = pd.read_csv('data.csv')
```

**Matplotlib**: Static plots
```python
import matplotlib.pyplot as plt
plt.plot(x, y)
```

**Seaborn**: Statistical visualizations
```python
import seaborn as sns
sns.scatterplot(data=df, x='col1', y='col2')
```

**Plotly**: Interactive plots
```python
import plotly.express as px
fig = px.scatter(df, x='col1', y='col2')
```

**Scikit-learn**: Machine learning, standard algorithms
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
```

**XGBoost**: Gradient boosting
```python
import xgboost as xgb
```

**GeoPandas**: Vector spatial data (shapefiles, points, polygons)
```python
import geopandas as gpd
gdf = gpd.read_file('data.shp')
```

**Rasterio**: Raster spatial data (GeoTIFFs, satellite imagery)
```python
import rasterio
with rasterio.open('raster.tif') as src:
    data = src.read(1)
```

**PyKrige**: Kriging interpolation
```python
from pykrige.ok import OrdinaryKriging
```

**Statsmodels**: Mixed models, advanced statistics
```python
import statsmodels.formula.api as smf
```

**PyTorch**: Deep learning, CNNs
```python
import torch
import torch.nn as nn
```

---

## Common Errors & Solutions

### ValueError: shapes not aligned
**Problem**: Matrix dimensions don't match
**Solution**: Check X.shape and y.shape, ensure compatible

### CRS Mismatch
**Problem**: Overlaying data with different CRS
**Solution**: Transform to same CRS first
```python
gdf2 = gdf2.to_crs(gdf1.crs)
```

### ConvergenceWarning in Mixed Models
**Problem**: Model didn't converge
**Solution**: Scale predictors, check for multicollinearity, increase max iterations

### Overfitting (high train R², low test R²)
**Solution**: Use regularization (Ridge/Lasso), reduce model complexity, get more data

### High prediction variance in Kriging
**Problem**: Predictions far from sample points
**Solution**: Collect more samples in high-variance areas, or accept uncertainty

---

## Useful Constants

**Earth radius**: 6371 km

**Degrees to radians**: multiply by π/180

**Acres to m²**: multiply by 4047

**Feet to meters**: multiply by 0.3048

**Common EPSG codes**:
- 4326: WGS84 (lat/lon)
- 3857: Web Mercator (Google Maps)
- 32616: UTM Zone 16N (Illinois area)

---

## Dataset Summary (from course repo)

Located in `/tmp/cpsc444-study/datasets/`:

- CSV files: Sample data points
- GeoPackage (.gpkg): Vector boundaries
- GeoTIFF (.tif): Raster data (elevation, imagery)

---

*Keep this reference handy while working through modules and projects!*
