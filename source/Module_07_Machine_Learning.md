# Module 07: Machine Learning & Ensemble Methods
## Random Forest, XGBoost, CNNs for Spatial Data

**Difficulty**: ⭐⭐⭐⭐⭐ Advanced
**Time Estimate**: 12-15 hours
**Prerequisites**: Modules 02 (Regression), 05 (Advanced regression)

---

## Module Overview

Classical statistics (regression, ANOVA) make assumptions about your data. Machine learning methods are more flexible - they can learn complex, non-linear patterns automatically. This module teaches powerful ML techniques particularly useful for spatial and agricultural data.

### What You'll Learn
- Ensemble methods (combining multiple models)
- Random Forest and XGBoost
- Convolutional Neural Networks (CNNs) for spatial patterns
- Pattern removal and detrending
- Imputation for missing data

### Why This Matters
Real-world patterns are complex:
- Non-linear relationships
- Interactions between variables
- Spatial patterns that classical methods miss
- ML can capture these automatically

---

## Core Concepts

### 1. Ensemble Methods - The Big Idea

**Simple analogy**: "Wisdom of the crowd" - many okay models together beat one great model.

**How it works**:
1. Train many models (each is okay, not perfect)
2. Combine their predictions
3. Result: Better than any single model

**Why it works**:
- Each model makes different mistakes
- Averaging reduces errors
- Captures different aspects of patterns

**Three main approaches**:
1. **Bagging**: Train models on different subsets of data (Random Forest)
2. **Boosting**: Train models sequentially, each fixing previous errors (XGBoost)
3. **Stacking**: Combine different model types with a meta-learner

---

### 2. Random Forest

**What it is**: Ensemble of decision trees, each trained on random subset of data.

**How a single decision tree works**:
```
                   Rainfall > 25"?
                   /           \
                 Yes            No
                 /               \
        Nitrogen > 100?      Yield = 150
            /      \
          Yes       No
          /          \
    Yield = 180  Yield = 165
```

**Simple explanation**: Ask yes/no questions about features, split data accordingly, predict at leaves.

**Random Forest combines many trees**:
1. Create 100+ trees
2. Each tree sees random subset of data (bagging)
3. Each split uses random subset of features
4. Average all predictions

**Why it's powerful**:
- Handles non-linear relationships automatically
- No assumptions about data distribution
- Resistant to overfitting (averaging reduces variance)
- Tells you which features are important

**Python example**:
```python
from sklearn.ensemble import RandomForestRegressor

# Create model (100 trees)
rf = RandomForestRegressor(
    n_estimators=100,  # Number of trees
    max_depth=10,      # Max tree depth
    min_samples_leaf=5, # Min samples per leaf
    random_state=42
)

# Fit
rf.fit(X_train, y_train)

# Predict
y_pred = rf.predict(X_test)

# Feature importance (which predictors matter most?)
importances = rf.feature_importances_
```

**Feature importance**: Shows which variables are most useful for predictions.

**When to use**:
- Many features
- Non-linear relationships
- Don't know which features matter
- Want robust predictions without much tuning

---

### 3. XGBoost (Extreme Gradient Boosting)

**What it is**: Builds trees sequentially - each new tree corrects previous errors.

**How boosting works**:
```
Tree 1: Makes predictions → Errors = Actual - Predicted
Tree 2: Predicts the errors from Tree 1
Tree 3: Predicts remaining errors from Tree 1 + Tree 2
...

Final prediction = Tree1 + Tree2 + Tree3 + ...
```

**Simple analogy**: Like editing a draft - first pass catches big mistakes, second pass catches smaller ones, etc.

**Why XGBoost is special**:
- **Regularization**: Prevents overfitting
- **Parallel processing**: Faster than other boosting
- **Handles missing data**: Built-in
- **Pruning**: Removes unhelpful branches

**Python example**:
```python
import xgboost as xgb

# Create model
xgb_model = xgb.XGBRegressor(
    n_estimators=100,     # Number of trees
    learning_rate=0.1,    # Step size (smaller = slower but better)
    max_depth=5,          # Max tree depth
    subsample=0.8,        # Fraction of data for each tree
    colsample_bytree=0.8, # Fraction of features per tree
    random_state=42
)

# Fit
xgb_model.fit(X_train, y_train)

# Predict
y_pred = xgb_model.predict(X_test)

# Feature importance
importances = xgb_model.feature_importances_
```

**Key hyperparameters**:
- `learning_rate`: How much each tree contributes (smaller = slower but often better)
- `max_depth`: Tree complexity
- `n_estimators`: Number of trees
- `subsample`: Fraction of data per tree (prevents overfitting)

**Random Forest vs XGBoost**:
- RF: Parallel, independent trees
- XGB: Sequential, each tree learns from previous
- RF: Faster to train, more robust
- XGB: Often slightly better accuracy, requires more tuning

---

### 4. Convolutional Neural Networks (CNNs) for Spatial Data

**What it is**: Neural networks that learn spatial patterns automatically.

**Originally from**: Computer vision (recognizing objects in images)

**Applied to spatial data**: Learn spatial patterns in agricultural/environmental rasters

**The key innovation: Convolution**

**Simple explanation**: Slide a small "filter" across your data, looking for patterns.

**Example**: Detecting high-yield patches in a field
```
Yield raster:
[150, 155, 160, 155, 150]
[155, 180, 185, 180, 155]  ← High-yield patch!
[160, 185, 190, 185, 160]
[155, 180, 185, 180, 155]
[150, 155, 160, 155, 150]

Filter (3×3):
[1, 1, 1]
[1, 1, 1]
[1, 1, 1]

Convolution = slide filter, compute sum at each position
→ Detects regions with high average yield
```

**CNN architecture for spatial data**:
```
Input raster → Conv layer → Activation → Conv layer → Output

Example:
Yield map (100×100) → Learn spatial filters → Predict true yield
                                               (removing noise/trends)
```

**Why CNNs for spatial ag data**:
- Learn spatial patterns automatically (hot spots, gradients)
- Remove systematic field trends
- Denoise spatial data
- Detect anomalies

**Use case: Pattern removal**

**Problem**: Yield data has systematic patterns (field slope, old fence lines) that aren't interesting.

**Solution**: Train CNN to predict these patterns, subtract them out.

```python
import torch
import torch.nn as nn

class SpatialCNN(nn.Module):
    def __init__(self):
        super(SpatialCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 1, kernel_size=3, padding=1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.conv3(x)
        return x

# Train CNN to learn spatial pattern
model = SpatialCNN()
# ... training code ...

# Predicted pattern
pattern = model(yield_raster)

# Detrended data
detrended_yield = yield_raster - pattern
```

**Result**: Removes large-scale spatial trends, reveals local variation.

---

### 5. CNN for Detrending vs Traditional Methods

**Traditional spatial detrending**: Fit polynomial surface, subtract it
```
z = β₀ + β₁x + β₂y + β₃x² + β₄y² + β₅xy
Detrended = Observed - Fitted surface
```

**CNN detrending**: Let network learn the pattern
- **Advantage**: Can learn complex, non-polynomial patterns
- **Advantage**: Adapts to actual data structure
- **Disadvantage**: Needs more data
- **Disadvantage**: "Black box" - harder to interpret

**Comparison**:
- **Polynomial**: Fast, interpretable, limited flexibility
- **CNN**: Slower, less interpretable, very flexible

**When to use CNN**:
- Large datasets (1000+ points)
- Complex spatial patterns
- Traditional methods don't capture the trend

---

### 6. Rook/Queen Contiguity vs CNN Filters

**Rook/Queen**: Fixed neighborhood structure
- Always uses immediate neighbors
- Same weights for all locations

**CNN filters**: Learned neighborhood structure
- Network learns which neighbors matter
- Different effective neighborhoods for different patterns

**Example**: Detecting weed patches
- Fixed contiguity might use 8 neighbors equally
- CNN might learn that diagonal neighbors matter more for this pattern

**Comparison (from course notebooks)**:
- Both can remove spatial autocorrelation
- CNN more flexible but needs more data
- Contiguity-based methods faster, more interpretable

---

### 7. Imputation with ML

**Problem**: Missing data in spatial/temporal datasets

**ML approach**: Train model to predict missing values based on:
- Nearby locations
- Time series patterns
- Correlated variables

**Example**:
```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor

# Use Random Forest to impute missing values
imputer = IterativeImputer(
    estimator=RandomForestRegressor(n_estimators=10),
    max_iter=10,
    random_state=42
)

# Impute
data_imputed = imputer.fit_transform(data_with_missing)
```

**How it works**:
1. Start with simple imputation (mean)
2. Predict each missing value using other variables
3. Iterate until convergence

**Better than mean imputation because**: Preserves relationships between variables.

---

## Course Materials

1. **[ENSEMBLMethods.ipynb](/tmp/cpsc444-study/python_notebooks/ENSEMBLMethods.ipynb)**
   - Bagging, Boosting, Stacking
   - Random Forest and XGBoost
   - Hyperparameter tuning

2. **[CNN_PatternRemover.ipynb](/tmp/cpsc444-study/python_notebooks/CNN_PatternRemover.ipynb)**
   - CNNs for detrending spatial data
   - Removing large-scale patterns
   - Residual learning

3. **[Field_Spatial_CNN_vs_RookQueen_Laplacian.ipynb](/tmp/cpsc444-study/python_notebooks/Field_Spatial_CNN_vs_RookQueen_Laplacian.ipynb)**
   - Comparing CNN filters to traditional contiguity
   - Spatial filtering approaches

4. **[SourceSeperatorCNN.ipynb](/tmp/cpsc444-study/python_notebooks/SourceSeperatorCNN.ipynb)**
   - Separating different spatial sources
   - Multi-scale spatial patterns

5. **[ImputationWorkflow.ipynb](/tmp/cpsc444-study/python_notebooks/ImputationWorkflow.ipynb)**
   - Missing data imputation strategies
   - ML-based imputation

---

## Key Concepts Summary

### Random Forest
- Ensemble of decision trees
- Bootstrap samples + random features
- Robust, handles non-linearity
- Easy to use, minimal tuning

### XGBoost
- Sequential boosting
- Each tree corrects previous errors
- Often highest accuracy
- Requires careful tuning

### CNNs for Spatial Data
- Learn spatial patterns via convolution
- Flexible, powerful
- Great for detrending and pattern detection
- Needs more data, less interpretable

---

## Study Checkpoints

### Can you explain...?
1. **How do ensemble methods improve predictions?**
2. **What's the difference between bagging (RF) and boosting (XGBoost)?**
3. **How do CNNs learn spatial patterns?**
4. **Why use CNNs for detrending instead of polynomials?**

### Can you do...?
1. **Fit Random Forest and interpret feature importance?**
2. **Tune XGBoost hyperparameters using cross-validation?**
3. **Apply CNN for spatial pattern removal?**
4. **Compare traditional and ML-based spatial methods?**

### Ready?
- [ ] I understand ensemble methods
- [ ] I can use Random Forest and XGBoost
- [ ] I understand CNNs for spatial data
- [ ] I know when to use ML vs traditional methods

**Next**: [Module 08: Specialized Applications](Module_08_Specialized_Applications.md)

---

*Machine learning unlocks patterns that classical methods can't capture - powerful tools for complex spatial data!*
