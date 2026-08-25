# Module 05: Advanced Regression
## Regularization, Geographically Weighted Regression & Hyperparameter Tuning

**Difficulty**: ⭐⭐⭐⭐ Advanced
**Time Estimate**: 8-10 hours
**Prerequisites**: Modules 02 (Regression), 03 (Spatial data), 04 (Spatial stats)

---

## Module Overview

Regular regression has limitations: it can overfit, perform poorly with many predictors, and assume relationships are the same everywhere. This module teaches advanced techniques to address these problems.

### What You'll Learn
- Regularization (Lasso, Ridge) to prevent overfitting
- Geographically Weighted Regression (GWR) for spatially-varying relationships
- Hyperparameter optimization
- Cross-validation strategies
- Non-linear curve fitting

### Why This Matters
Real-world relationships are rarely simple:
- Fertilizer response might differ across a field (need GWR)
- With 50 predictors, regular regression overfits (need regularization)
- Model performance depends on parameter choices (need optimization)

---

## Core Concepts

### 1. The Overfitting Problem

**What is overfitting?** Model fits training data TOO well, including noise, so it performs poorly on new data.

**Simple analogy**: Memorizing test answers vs understanding concepts. Memorization works on that exact test but fails on similar questions.

**Example**:
- Training data: 95% accuracy
- Test data: 60% accuracy
- **Problem**: Overfit!

**Solution**: Regularization

---

### 2. Ridge Regression (L2 Regularization)

**What it does**: Penalizes large coefficients, forcing the model to use all predictors but keep coefficients small.

**Formula**:
```
Minimize: Σ(y - ŷ)² + λΣβ²
          ↑            ↑
     prediction     penalty
        error       on large
                   coefficients
```

**Simple explanation**: Find coefficients that predict well BUT keep them small. The λ (lambda) parameter controls the trade-off.

**When to use**: Many correlated predictors (multicollinearity)

**Example**:
```python
from sklearn.linear_model import Ridge

# λ = alpha in sklearn
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

# Coefficients will be smaller than ordinary regression
print(ridge.coef_)
```

**Effect of λ**:
- λ = 0: Regular regression (no penalty)
- λ small: Slight penalty
- λ large: All coefficients shrink toward zero

---

### 3. Lasso Regression (L1 Regularization)

**What it does**: Penalizes coefficients, but can set some to EXACTLY ZERO (feature selection).

**Formula**:
```
Minimize: Σ(y - ŷ)² + λΣ|β|
```

**Simple explanation**: Like Ridge, but can completely eliminate unimportant predictors.

**When to use**: Want to identify which predictors matter most

**Example**:
```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)

# Some coefficients will be exactly 0
print(lasso.coef_)
# Example output: [2.3, 0, 1.5, 0, 0, 3.1, 0]
#                       ↑     ↑  ↑      ↑
#                   These predictors were eliminated
```

**Ridge vs Lasso**:
- Ridge: Keeps all predictors, shrinks coefficients
- Lasso: Eliminates some predictors entirely
- Lasso is easier to interpret (fewer non-zero coefficients)

---

### 4. Geographically Weighted Regression (GWR)

**The problem**: Regular regression assumes relationships are the same everywhere. But what if fertilizer response differs across a field?

**Solution**: Fit LOCAL regression models - different coefficients for different locations.

**Simple analogy**: Instead of one "average" recipe for the whole country, you have regional variations (Southern cooking, New England cooking, etc.).

**How it works**:

1. Choose a location to predict
2. Weight nearby data points more heavily
3. Fit a regression using those weights
4. Repeat for every location

**Weighting function** (Gaussian kernel):
```
w_i = exp(-(d_i / bandwidth)²)
```
- `d_i` = distance from prediction location to data point i
- Closer points get higher weights
- `bandwidth` controls how far influence extends

**Example**:
```python
# Conceptual example (simplified)
def gwr_predict(x0, y0, X, Y, values, bandwidth):
    """Predict at location (x0, y0) using GWR"""

    # Calculate distances to all data points
    distances = np.sqrt((X - x0)**2 + (Y - y0)**2)

    # Calculate weights (Gaussian kernel)
    weights = np.exp(-(distances / bandwidth)**2)

    # Fit weighted regression
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(predictors, values, sample_weight=weights)

    # Predict at this location
    return model.predict(new_predictors)
```

**Output**: Different coefficients at every location!

**Example interpretation**:
- West side of field: Rainfall coefficient = 3.5 (rain really helps here)
- East side of field: Rainfall coefficient = 1.2 (rain helps less)
- **Conclusion**: Water management could be spatially targeted

---

### 5. Hyperparameter Tuning

**What are hyperparameters?** Settings you choose BEFORE fitting the model (like λ in Ridge/Lasso, bandwidth in GWR).

**The challenge**: How do you choose the best value?

#### Grid Search

**What**: Try every combination of parameters from a list.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge

# Define parameter grid
param_grid = {
    'alpha': [0.1, 1.0, 10, 100, 1000]
}

# Grid search with cross-validation
grid_search = GridSearchCV(
    Ridge(),
    param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='r2'
)

grid_search.fit(X_train, y_train)

print(f"Best alpha: {grid_search.best_params_}")
print(f"Best R²: {grid_search.best_score_}")
```

**Pros**: Guaranteed to find best combination in grid
**Cons**: Slow with many parameters

#### Random Search

**What**: Try random combinations.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform

# Define parameter distributions
param_dist = {
    'alpha': uniform(0.1, 1000)  # Uniform distribution
}

random_search = RandomizedSearchCV(
    Ridge(),
    param_dist,
    n_iter=50,  # Try 50 random combinations
    cv=5,
    scoring='r2'
)

random_search.fit(X_train, y_train)
```

**Pros**: Faster, explores more space
**Cons**: Might miss optimal value

#### Bayesian Optimization

**What**: Intelligently choose next parameters to try based on previous results.

```python
from skopt import BayesSearchCV

# More efficient than random search
bayes_search = BayesSearchCV(
    Ridge(),
    {'alpha': (0.1, 1000, 'log-uniform')},
    n_iter=30,
    cv=5
)

bayes_search.fit(X_train, y_train)
```

**Pros**: Most efficient
**Cons**: More complex

---

### 6. Cross-Validation

**The problem**: If you test on the same data you trained on, you can't detect overfitting.

**Solution**: Split data into folds, train on some, test on others.

#### K-Fold Cross-Validation

```
Dataset split into 5 folds:
[1] [2] [3] [4] [5]

Iteration 1: Train on [2][3][4][5], test on [1]
Iteration 2: Train on [1][3][4][5], test on [2]
Iteration 3: Train on [1][2][4][5], test on [3]
...
```

**Average performance across all folds = true model quality**

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Ridge

scores = cross_val_score(
    Ridge(alpha=10),
    X, y,
    cv=5,  # 5-fold
    scoring='r2'
)

print(f"Mean R²: {scores.mean()}")
print(f"Std: {scores.std()}")
```

#### Spatial Cross-Validation

**Problem**: With spatial data, nearby points are correlated. Random CV splits put correlated data in train AND test sets!

**Solution**: Spatial CV - test set is spatially separated from training set.

**Example**: Leave out entire regions
```python
# Group by spatial clusters
from sklearn.model_selection import GroupKFold

# Assign each point to a spatial cluster
clusters = assign_spatial_clusters(coordinates)

gkf = GroupKFold(n_splits=5)
for train_idx, test_idx in gkf.split(X, y, groups=clusters):
    # Train and test sets are spatially separated
    ...
```

---

### 7. Non-linear Curve Fitting

**Problem**: Relationships aren't always linear!

**Example**: Yield vs fertilizer
- Too little: Low yield
- Optimal amount: High yield
- Too much: Yield drops (toxicity)
- **Shape**: Curve, not line!

**Solution**: Fit non-linear models

```python
from scipy.optimize import curve_fit

# Define non-linear function (e.g., quadratic)
def quadratic(x, a, b, c):
    return a*x**2 + b*x + c

# Fit
params, covariance = curve_fit(
    quadratic,
    fertilizer_amounts,
    yields
)

# Predict
predicted_yield = quadratic(new_fertilizer, *params)
```

**Common non-linear forms**:
- Quadratic: `y = ax² + bx + c`
- Exponential: `y = a × exp(bx)`
- Logistic (S-curve): `y = L / (1 + exp(-k(x-x₀)))`

---

## Course Materials

1. **[Regularization.ipynb](/tmp/cpsc444-study/python_notebooks/Regularization.ipynb)** - Lasso & Ridge
2. **[CurveFittingAlgorithms.ipynb](/tmp/cpsc444-study/python_notebooks/CurveFittingAlgorithms.ipynb)** - Non-linear fits
3. **[Automobile-nonlinearity.ipynb](/tmp/cpsc444-study/python_notebooks/Automobile-nonlinearity.ipynb)** - Real example
4. **[GeographicallyWeightedRegression_Kernels.ipynb](/tmp/cpsc444-study/python_notebooks/GeographicallyWeightedRegression_Kernels.ipynb)** - GWR theory
5. **[GWR_CaseStudy.ipynb](/tmp/cpsc444-study/python_notebooks/GWR_CaseStudy.ipynb)** - GWR application
6. **[GWR_CaseStudy_Updated.ipynb](/tmp/cpsc444-study/python_notebooks/GWR_CaseStudy_Updated.ipynb)** - Updated examples

---

## Study Checkpoints

### Can you explain...?
1. **What's the difference between Ridge and Lasso?**
2. **Why is GWR better than regular regression for spatial data?**
3. **What does λ (lambda) control in regularization?**
4. **Why do we need cross-validation?**

### Can you do...?
1. **Fit Ridge and Lasso models and compare results?**
2. **Use GridSearchCV to find optimal hyperparameters?**
3. **Implement basic GWR for a spatial dataset?**
4. **Fit non-linear curves to data?**

### Ready?
- [ ] I understand Ridge and Lasso regularization
- [ ] I can perform GWR and interpret local coefficients
- [ ] I know how to tune hyperparameters
- [ ] I understand cross-validation strategies

**Next**: [Module 06: Mixed Models](Module_06_Mixed_Models.md)

---

*Advanced regression techniques unlock the complexity in real-world data!*
