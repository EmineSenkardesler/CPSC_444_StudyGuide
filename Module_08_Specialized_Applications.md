# Module 08: Specialized Applications
## Crop Modeling, Multi-Source Data Fusion & Real-World Integration

**Difficulty**: ⭐⭐⭐⭐⭐ Expert
**Time Estimate**: 10-15 hours
**Prerequisites**: Multiple previous modules (this is the capstone!)

---

## Module Overview

This module brings together everything you've learned and applies it to real-world problems. You'll see how spatial statistics, regression, machine learning, and domain knowledge combine to solve complex agricultural and environmental challenges.

### What You'll Learn
- Mechanistic crop growth models
- Process-based simulation
- Multi-source spatial data fusion
- Integrated prediction frameworks
- Genomic data applications
- Mathematical foundations (convolution)

### Why This Matters
Real applications require:
- Combining multiple data sources (satellite, weather, soil, management)
- Integrating statistical and process-based models
- Domain-specific expertise
- This module shows you how it all comes together

---

## Core Concepts

### 1. Mechanistic vs Statistical Models

**Statistical models** (what you've learned so far):
- Learn patterns from data
- Example: Yield = f(rainfall, temperature, nitrogen)
- **Strength**: Flexible, data-driven
- **Weakness**: Can't extrapolate beyond training data

**Mechanistic (process-based) models**:
- Simulate underlying biological/physical processes
- Example: Photosynthesis equations → growth → yield
- **Strength**: Based on science, can extrapolate
- **Weakness**: Complex, needs many parameters

**Best approach**: Combine both!
- Use mechanistic model for structure
- Use statistical methods to calibrate parameters
- Use ML to capture residual patterns

---

### 2. Crop Growth Modeling Basics

**The core process**: Light + CO₂ + Water → Photosynthesis → Biomass → Yield

**Simple mechanistic model**:
```
Light interception = LAI × (1 - exp(-k × LAI))
  where LAI = Leaf Area Index
        k = extinction coefficient

Photosynthesis = ε × Intercepted light
  where ε = light use efficiency

Biomass(t+1) = Biomass(t) + Photosynthesis - Respiration

Yield = Biomass × HI
  where HI = Harvest Index (fraction going to grain)
```

**Simple explanation**:
- More leaves → intercept more light
- More light → more photosynthesis → more growth
- But plants also respire (use energy)
- At harvest, only part of biomass is grain (harvest index)

**Parameters to estimate**:
- k (light extinction)
- ε (efficiency)
- Respiration rate
- HI (harvest index)

**How spatial data helps**:
- Satellite imagery → estimate LAI over space
- Weather stations → temperature, radiation
- Spatial variation in parameters → better predictions

---

### 3. Photosynthesis Toy Models

**Simplified Farquhar model** (photosynthesis rate):
```
A = min(Wc, Wj) - Rd

where:
  Wc = Rubisco-limited rate
  Wj = Light-limited rate
  Rd = Dark respiration
  A = Net photosynthesis
```

**Simple explanation**:
- Two limiting processes: enzyme (Rubisco) and light
- Photosynthesis limited by whichever is lower
- Subtract respiration to get net

**Temperature effects**:
```
Optimal temperature: ~25-30°C
Too cold: Enzymes slow
Too hot: Enzymes denature
```

**Why model this?**:
- Predict response to climate change
- Understand heat stress
- Optimize planting dates

**Integration with spatial data**:
- Map temperature across landscape
- Predict spatial variation in photosynthesis
- Identify heat-stress zones

---

### 4. Multi-Source Spatial Data Fusion

**The challenge**: Combine data from multiple sources with:
- Different spatial resolutions
- Different temporal frequencies
- Different coverage areas
- Different measurement errors

**Example data sources for yield prediction**:
1. **Satellite imagery**: 10m resolution, every 5 days, NDVI
2. **Weather stations**: Point data, daily, temperature/rainfall
3. **Soil sampling**: Irregular points, one-time, nutrients
4. **Yield monitor**: 5m resolution, annual, actual yield

**How do you combine these?**

#### Approach 1: Spatial Regression Framework

```python
# 1. Interpolate all sources to common grid
soil_grid = kriging(soil_samples, target_grid)
weather_grid = interpolate(weather_stations, target_grid)
ndvi_grid = resample(satellite_ndvi, target_grid)

# 2. Stack as predictors
X = np.stack([soil_grid, weather_grid, ndvi_grid], axis=-1)

# 3. Fit model (e.g., Random Forest)
model = RandomForestRegressor()
model.fit(X, yield_observations)

# 4. Predict everywhere
yield_predicted = model.predict(X_future)
```

#### Approach 2: Hierarchical Bayesian Model

**Idea**: Model each data source's relationship to underlying process, account for uncertainty.

```
True yield (latent) → Observed yield (noisy)
True yield ← f(True NDVI, True soil, True weather)
  where each "True" is estimated from observations
```

**Advantage**: Properly propagates uncertainty from all sources.

---

### 5. Multi-Scale Spatial Patterns

**Real spatial data has patterns at multiple scales**:

**Large scale** (100s of meters):
- Soil type changes
- Topographic effects
- Management zones

**Medium scale** (10s of meters):
- Previous crop residue
- Drainage patterns
- Equipment patterns

**Small scale** (meters):
- Individual plant variation
- Localized pests/disease
- Measurement noise

**Challenge**: Separate these scales!

**Approach 1: Wavelet decomposition**
- Decompose signal into different frequency components
- Like musical notes (low frequency = base note, high frequency = overtones)

**Approach 2: Multi-scale CNN**
- Different filter sizes capture different scales
- Combine information across scales

**Why it matters**:
- Management decisions at different scales
- Understanding which processes operate at which scales
- Removing nuisance patterns at one scale to see patterns at another

---

### 6. Genomic Data Application (Arabidopsis FAAs)

**Context**: Applying spatial/statistical methods to genomic data.

**The data**: Functional amino acid sequences (FAAs) across genome

**Spatial analogy**:
- Genome position is like spatial location
- Gene expression is like spatial measurement
- Correlation structure along genome similar to spatial autocorrelation

**Methods applied**:
- Semivariograms along genome
- Detecting clusters of related genes
- Smoothing noisy expression data

**Key insight**: Spatial statistics apply to ANY data with distance/correlation structure, not just geographic space!

---

### 7. Complete Prediction Framework

**Integrating all course concepts**:

```
Step 1: Data acquisition and preprocessing
  - Load spatial data (rasters, vectors)
  - Check and align CRS
  - Handle missing data (imputation)

Step 2: Exploratory spatial analysis
  - Visualize spatial patterns
  - Calculate semivariograms
  - Identify spatial autocorrelation
  - Detect trends

Step 3: Detrending (if needed)
  - Remove large-scale spatial patterns (polynomial or CNN)
  - Analyze residuals

Step 4: Feature engineering
  - Create derived variables
  - Lag features (spatial neighbors)
  - Temporal features

Step 5: Model selection
  - Simple baseline (linear regression)
  - Spatial regression (GWR if relationships vary spatially)
  - Mixed models (if hierarchical structure)
  - ML methods (RF, XGBoost for non-linearity)
  - Ensemble (combine multiple approaches)

Step 6: Model evaluation
  - Spatial cross-validation (not random!)
  - Multiple metrics (R², RMSE, spatial autocorrelation of residuals)
  - Validate on held-out years/locations

Step 7: Prediction and uncertainty
  - Generate predictions
  - Estimate uncertainty (kriging variance, bootstrap, etc.)
  - Visualize on maps

Step 8: Interpretation
  - Feature importance
  - Partial dependence plots
  - Spatial patterns in predictions
  - Domain expertise validation
```

**This is the complete workflow!**

---

### 8. Convolution Mathematics (Bonus Theory)

**Convolution operation** (from CNN module, but deeper):

**Definition**:
```
(f ∗ g)(t) = ∫ f(τ) g(t - τ) dτ
```

**Discrete version (for images/rasters)**:
```
(I ∗ K)(i,j) = ΣΣ I(i+m, j+n) × K(m, n)
```

**What it means**:
- Slide filter K over image I
- At each position, multiply and sum
- Result: Filtered image

**Properties proven in notebook**:
- Commutative: f ∗ g = g ∗ f
- Associative: (f ∗ g) ∗ h = f ∗ (g ∗ h)
- Distributive: f ∗ (g + h) = (f ∗ g) + (f ∗ h)

**Why this matters for CNNs**:
- Convolution is mathematically well-founded
- Properties guarantee certain behaviors
- Understanding helps debug CNN issues

---

## Course Materials

1. **[Crop_Modeling_Example.ipynb](/tmp/cpsc444-study/python_notebooks/Crop_Modeling_Example.ipynb)**
   - Mechanistic crop growth simulation
   - Parameter estimation
   - Sensitivity analysis

2. **[Photosynthesis_ToyModels.ipynb](/tmp/cpsc444-study/python_notebooks/Photosynthesis_ToyModels.ipynb)**
   - Simplified photosynthesis models
   - Temperature response curves
   - Integration with environmental data

3. **[ArabidopsisFAAs.ipynb](/tmp/cpsc444-study/python_notebooks/ArabidopsisFAAs.ipynb)**
   - Applying spatial methods to genomic data
   - Correlation along genome
   - Clustering and smoothing

4. **[Multi_Source_Spatial_Prediction-v2.ipynb](/tmp/cpsc444-study/python_notebooks/Multi_Source_Spatial_Prediction-v2.ipynb)**
   - Combining multiple data sources
   - Spatial data fusion methods
   - Integrated predictions

5. **[Multi_Source_Spatial_Framework_Complete.ipynb](/tmp/cpsc444-study/python_notebooks/Multi_Source_Spatial_Framework_Complete.ipynb)**
   - Complete prediction framework
   - End-to-end workflow
   - Best practices

6. **[ConvolutionProof+Operation.ipynb](/tmp/cpsc444-study/python_notebooks/ConvolutionProof+Operation.ipynb)**
   - Mathematical foundations of convolution
   - Proofs of key properties
   - Applications to spatial filtering

---

## Study Checkpoints

### Can you explain...?
1. **What's the difference between mechanistic and statistical models?**
2. **How do you combine data from multiple sources with different resolutions?**
3. **Why apply spatial methods to genomic data?**
4. **What are the key steps in a complete spatial prediction framework?**

### Can you do...?
1. **Set up a simple crop growth model?**
2. **Integrate multiple spatial data sources?**
3. **Apply the complete prediction framework to a new problem?**
4. **Validate predictions properly with spatial cross-validation?**

### Course Complete!

Congratulations! You've mastered:
- [ ] Python foundations and statistics
- [ ] Regression and classification
- [ ] Geospatial data analysis
- [ ] Spatial statistics and autocorrelation
- [ ] Advanced regression techniques
- [ ] Mixed models for hierarchical data
- [ ] Machine learning methods
- [ ] Real-world applications and integration

**What's next?**
- Apply these skills to your own research/projects
- Explore advanced topics in your area of interest
- Contribute to open-source spatial data science projects
- Keep practicing - mastery comes through application!

---

## Final Project Ideas

To solidify your learning, try a complete project:

1. **Yield prediction across multiple fields**
   - Combine satellite, weather, soil data
   - Compare multiple methods
   - Generate prediction maps with uncertainty

2. **Spatial disease monitoring**
   - Detect disease clusters
   - Predict spread using spatial models
   - Recommend targeted interventions

3. **Climate change impact assessment**
   - Use crop models with future climate scenarios
   - Spatial variation in impacts
   - Identify vulnerable regions

4. **Precision agriculture zone delineation**
   - Multi-source data fusion
   - Clustering algorithms
   - Management zone recommendations

5. **Environmental monitoring network optimization**
   - Use kriging variance to identify optimal sample locations
   - Minimize uncertainty with fixed budget
   - Adaptive sampling strategies

---

*You've completed the journey from Python basics to advanced spatial data science - now apply these powerful tools to make real-world impact!*
