# Module 02: Statistical Foundations
## Multiple Regression, Logistic Regression & Model Evaluation

**Difficulty**: ⭐⭐ Intermediate
**Time Estimate**: 5-7 hours
**Prerequisites**: Module 01 (Python basics, simple regression, statistics)

---

## Module Overview

In Module 01, you learned simple linear regression - predicting one variable from another (like yield from rainfall). In this module, you'll learn how to use MULTIPLE variables to make predictions (like yield from rainfall AND temperature AND soil type). You'll also learn how to make yes/no predictions (logistic regression) and how to evaluate whether your models are actually good.

### What You'll Learn
- Multiple regression (using several predictors at once)
- Matrix-based solutions for regression
- Logistic regression (for yes/no outcomes)
- How to evaluate model quality
- Correlation vs causation
- Model assumptions and diagnostics

### Why This Matters
Real-world outcomes usually depend on multiple factors, not just one:
- Crop yield depends on rainfall, temperature, soil nutrients, planting date, etc.
- Disease occurrence depends on temperature, humidity, crop variety, previous crops, etc.
- Knowing how to use multiple predictors and evaluate model quality is essential for practical data analysis.

---

## Learning Objectives

By the end of this module, you will be able to:
- [ ] Build multiple regression models with several predictors
- [ ] Understand the matrix formulation of regression
- [ ] Apply logistic regression for binary classification
- [ ] Evaluate models using R², MSE, and confusion matrices
- [ ] Interpret regression coefficients correctly
- [ ] Assess model assumptions
- [ ] Distinguish correlation from causation

---

## Core Concepts

### 1. Multiple Linear Regression

**What it is**: Predicting one outcome variable using TWO OR MORE predictor variables.

**Simple regression**: `Yield = b₀ + b₁ × Rainfall`
**Multiple regression**: `Yield = b₀ + b₁ × Rainfall + b₂ × Temperature + b₃ × Nitrogen`

**Simple explanation**: Instead of drawing a line through points (simple regression), you're fitting a plane or higher-dimensional surface through your data (multiple regression).

**Real-world example**: Predicting corn yield

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Predictor variables (X) - each column is a different predictor
X = np.array([
    [30, 75, 120],  # Field 1: 30" rain, 75°F avg temp, 120 lb/acre nitrogen
    [25, 78, 100],  # Field 2
    [35, 72, 130],  # Field 3
    [28, 77, 115],  # Field 4
    [32, 74, 125],  # Field 5
])

# Outcome variable (y)
y = np.array([175, 160, 185, 170, 180])  # Yields in bushels/acre

# Fit the model
model = LinearRegression()
model.fit(X, y)

# The equation is:
# Yield = intercept + (coef₁ × Rainfall) + (coef₂ × Temp) + (coef₃ × Nitrogen)
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Predict yield for new field: 31" rain, 76°F, 120 lb/acre nitrogen
new_field = np.array([[31, 76, 120]])
predicted_yield = model.predict(new_field)
print(f"Predicted yield: {predicted_yield[0]:.1f} bushels/acre")
```

**Interpreting coefficients**:
If the rainfall coefficient is 2.5, it means: "Holding temperature and nitrogen constant, each additional inch of rain increases yield by 2.5 bushels/acre."

This is key: each coefficient shows the effect of that variable when ALL OTHER variables are held constant.

---

### 2. Matrix Formulation

**What it is**: A mathematical way to solve regression problems using matrices and linear algebra.

**The normal equation**: `β = (XᵀX)⁻¹Xᵀy`

**Simple explanation**: This formula gives you all the regression coefficients (β) in one calculation.

**Breaking it down**:
- `X` = matrix of all your predictor values
- `Xᵀ` = X transposed (flipped rows and columns)
- `y` = vector of outcome values
- `β` = the coefficients you're solving for
- `⁻¹` = matrix inverse (like division for matrices)

**Why it matters**: This is what's happening "under the hood" when you use regression functions. Understanding it helps you:
- Know what assumptions are being made
- Understand when regression might fail (like when XᵀX can't be inverted)
- Debug problems with your models

**Simple example with 2 predictors**:

```python
import numpy as np

# Predictor matrix X (add column of 1s for intercept)
X = np.array([
    [1, 30, 120],  # 1, rainfall, nitrogen
    [1, 25, 100],
    [1, 35, 130],
    [1, 28, 115],
    [1, 32, 125],
])

y = np.array([175, 160, 185, 170, 180])

# Solve using normal equation: β = (XᵀX)⁻¹Xᵀy
XtX = X.T @ X  # @ is matrix multiplication
XtX_inv = np.linalg.inv(XtX)
Xty = X.T @ y
beta = XtX_inv @ Xty

print(f"Coefficients: {beta}")
# beta[0] = intercept
# beta[1] = rainfall coefficient
# beta[2] = nitrogen coefficient
```

**When this fails**: If two predictors are perfectly correlated (multicollinearity), XᵀX can't be inverted. Example: including both "area in acres" and "area in hectares" as separate predictors.

---

### 3. Logistic Regression

**What it is**: Used when you want to predict a yes/no outcome (will it rain? will the crop fail? will the pest appear?).

**Simple explanation**: Regular regression predicts numbers. Logistic regression predicts probabilities (0 to 1), which you can interpret as "probability of yes."

**How it works**: Uses a sigmoid (S-shaped) function to squeeze predictions between 0 and 1:

```
P(yes) = 1 / (1 + e^(-z))

where z = b₀ + b₁x₁ + b₂x₂ + ...
```

**Real-world example**: Predicting if a field will experience drought stress

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

# Features: [rainfall (inches), temperature (°F)]
X = np.array([
    [35, 72],  # Good rain, moderate temp
    [15, 85],  # Low rain, hot
    [40, 70],  # Excellent conditions
    [12, 88],  # Drought risk!
    [30, 78],  # Moderate
    [10, 90],  # High drought risk
    [38, 73],  # Good
])

# Outcome: 1 = drought stress, 0 = no stress
y = np.array([0, 1, 0, 1, 0, 1, 0])

# Fit logistic regression
model = LogisticRegression()
model.fit(X, y)

# Predict for new field: 20" rain, 83°F
new_field = np.array([[20, 83]])

# Get probability of drought stress
prob_drought = model.predict_proba(new_field)[0, 1]
print(f"Probability of drought stress: {prob_drought:.2%}")

# Get yes/no prediction (uses 0.5 as cutoff by default)
prediction = model.predict(new_field)[0]
print(f"Prediction: {'Drought stress' if prediction == 1 else 'No stress'}")
```

**Key difference from linear regression**:
- Linear: Predicts any number (-∞ to +∞)
- Logistic: Predicts probability (0 to 1), then converts to yes/no

**Understanding the sigmoid curve**:
- When z is very negative → probability ≈ 0
- When z = 0 → probability = 0.5
- When z is very positive → probability ≈ 1

The curve is S-shaped, transitioning smoothly from 0 to 1.

---

### 4. Decision Boundaries

**What it is**: The line (or surface) that separates "predict yes" from "predict no" in classification.

**Simple explanation**: Imagine plotting all your data points on a graph, with positive outcomes in red and negative outcomes in blue. The decision boundary is the line that best separates red from blue.

**Example with logistic regression**:

In 1D (one predictor):
- If temperature > 85°F → predict drought
- Decision boundary is a single point: 85°F

In 2D (two predictors):
- Decision boundary is a line dividing the space
- Example: `0.5 × Rainfall + 0.3 × Temperature = threshold`

In 3D (three predictors):
- Decision boundary is a plane

**Why it matters**: Visualizing decision boundaries helps you understand what your model is doing. If the boundary doesn't make sense, your model might not be capturing the right patterns.

---

### 5. Model Evaluation Metrics

How do you know if your model is good? Use these metrics:

#### For Regression Models (predicting numbers):

**1. R-squared (R²)**
- **What**: Proportion of variance explained by the model
- **Range**: 0 to 1 (higher is better)
- **Simple explanation**: If R² = 0.85, your model explains 85% of the variation in the outcome

```python
from sklearn.metrics import r2_score

r2 = r2_score(y_true, y_predicted)
```

**Interpretation**:
- R² = 0.9+: Excellent fit
- R² = 0.7-0.9: Good fit
- R² = 0.5-0.7: Moderate fit
- R² < 0.5: Poor fit (model isn't capturing much)

**2. Mean Squared Error (MSE)**
- **What**: Average of squared differences between predicted and actual values
- **Range**: 0 to ∞ (lower is better)
- **Simple explanation**: Measures how far off your predictions are on average

```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_true, y_predicted)
rmse = np.sqrt(mse)  # Root MSE is in same units as y
```

**Example**: If predicting yield and RMSE = 15, your predictions are typically off by about 15 bushels/acre.

**3. Mean Absolute Error (MAE)**
- **What**: Average absolute difference (doesn't square the errors)
- **Simple explanation**: On average, how far off are predictions?

```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_true, y_predicted)
```

**MSE vs MAE**: MSE punishes large errors more (because of squaring). Use MSE when large errors are especially bad, MAE when all errors are equally important.

#### For Classification Models (yes/no predictions):

**1. Confusion Matrix**

**What it is**: A table showing correct and incorrect predictions:

```
                   Predicted: No    Predicted: Yes
Actual: No         True Negative    False Positive
Actual: Yes        False Negative   True Positive
```

**Simple example**: Predicting disease in plants

```python
from sklearn.metrics import confusion_matrix

y_true = [0, 1, 0, 1, 1, 0, 1, 0]  # Actual disease status
y_pred = [0, 1, 0, 0, 1, 0, 1, 1]  # Model predictions

cm = confusion_matrix(y_true, y_pred)
print(cm)
# [[3, 1],     3 correct "no disease", 1 false alarm
#  [1, 3]]     1 missed disease, 3 correct "disease"
```

**2. Accuracy**
- **What**: Percentage of correct predictions
- **Formula**: (TP + TN) / Total

```python
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_true, y_pred)  # 0.75 = 75% correct
```

**Warning**: Accuracy can be misleading with imbalanced classes! If disease is rare (only 5% of plants), a model that always predicts "no disease" gets 95% accuracy but is useless.

**3. Precision and Recall**

**Precision**: Of all the "yes" predictions, how many were right?
- Formula: TP / (TP + FP)
- Example: Of all plants predicted diseased, what % actually were?

**Recall (Sensitivity)**: Of all actual "yes" cases, how many did we catch?
- Formula: TP / (TP + FN)
- Example: Of all actually diseased plants, what % did we detect?

```python
from sklearn.metrics import precision_score, recall_score

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
```

**Trade-off**: You can increase recall by predicting "yes" more often, but this decreases precision (more false alarms). There's usually a balance to strike.

**4. ROC Curve and AUC**

**ROC curve**: Plots true positive rate vs false positive rate at different prediction thresholds

**AUC (Area Under Curve)**: Summary metric for ROC curve
- **Range**: 0.5 to 1.0
- **Simple explanation**:
  - AUC = 1.0: Perfect classifier
  - AUC = 0.9: Excellent
  - AUC = 0.8: Good
  - AUC = 0.7: Fair
  - AUC = 0.5: Random guessing (useless)

```python
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Get probability predictions
y_probs = model.predict_proba(X_test)[:, 1]

# Calculate AUC
auc = roc_auc_score(y_true, y_probs)

# Plot ROC curve
fpr, tpr, thresholds = roc_curve(y_true, y_probs)
plt.plot(fpr, tpr, label=f'AUC = {auc:.2f}')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

---

### 6. Correlation vs Causation

**Critical concept**: Just because two things are correlated doesn't mean one causes the other!

**Classic example**: Ice cream sales and drowning deaths are correlated. Does ice cream cause drowning? No! Both increase in summer (confounding variable: weather).

**In agriculture**:
- Yield and fertilizer price might be correlated (both go up during good economic years)
- But fertilizer price doesn't cause yield; economic conditions affect both

**How to think about it**:
1. **Correlation**: Two variables move together
2. **Causation**: One variable directly causes changes in the other

**What regression shows**: Regression finds correlation (association), not causation. To establish causation, you need:
- Controlled experiments (randomized trials)
- Temporal precedence (cause happens before effect)
- No alternative explanations (rule out confounders)

**Practical advice**: Use regression to find relationships and generate hypotheses, but be cautious about claiming causation without experimental evidence.

---

## Course Materials

### Primary Notebooks

1. **[python_notebooks/MultipleRegression.ipynb](/tmp/cpsc444-study/python_notebooks/MultipleRegression.ipynb)**
   - Matrix solutions for multiple regression
   - Normal equation implementation
   - Understanding XᵀX and matrix inversion

2. **[python_notebooks/Correlation&MLR.ipynb](/tmp/cpsc444-study/python_notebooks/Correlation&MLR.ipynb)**
   - Correlation analysis
   - Multiple linear regression examples
   - Relationship between correlation and regression

3. **[python_notebooks/LogisticRegression.ipynb](/tmp/cpsc444-study/python_notebooks/LogisticRegression.ipynb)**
   - Logistic regression implementation
   - Gradient descent algorithm
   - Sigmoid function
   - Decision boundaries in 1D, 2D, and 3D
   - Classification metrics

4. **[python_notebooks/GaltonSeeds.ipynb](/tmp/cpsc444-study/python_notebooks/GaltonSeeds.ipynb)**
   - Historical example of regression
   - Understanding regression to the mean
   - Practical regression application

5. **[python_notebooks/GoF.ipynb](/tmp/cpsc444-study/python_notebooks/GoF.ipynb)**
   - Goodness of fit testing
   - Model diagnostics
   - Checking regression assumptions

---

## Key Formulas

### Multiple Regression
```
y = β₀ + β₁x₁ + β₂x₂ + β₃x₃ + ... + ε
```
**In words**: Outcome = intercept + (coef × predictor₁) + (coef × predictor₂) + ... + error

### Matrix Form of Regression
```
β = (XᵀX)⁻¹Xᵀy
```
**In words**: Coefficients = (X-transpose times X, inverted) times (X-transpose times y)

### Logistic Regression (Sigmoid)
```
P(y=1) = 1 / (1 + e^(-z))
where z = β₀ + β₁x₁ + β₂x₂ + ...
```
**In words**: Probability of "yes" is determined by a sigmoid curve applied to the linear combination of predictors.

### Mean Squared Error
```
MSE = (1/n) Σ(yᵢ - ŷᵢ)²
```
**In words**: Average of squared differences between actual and predicted values.

### R-squared
```
R² = 1 - (SS_residual / SS_total)
```
**In words**: Proportion of variance explained = 1 - (unexplained variance / total variance)

---

## Study Checkpoints

Before moving to Module 03, make sure you can answer these questions:

### Can you explain...?

1. **What's the difference between simple and multiple regression?**
   <details>
   <summary>Click to check</summary>
   Simple regression uses ONE predictor to predict the outcome (y = b₀ + b₁x). Multiple regression uses TWO OR MORE predictors (y = b₀ + b₁x₁ + b₂x₂ + ...). Multiple regression can capture more complex relationships but requires more data.
   </details>

2. **What does a regression coefficient mean in multiple regression?**
   <details>
   <summary>Click to check</summary>
   Each coefficient shows the change in the outcome for a one-unit increase in that predictor, HOLDING ALL OTHER PREDICTORS CONSTANT. Example: if rainfall coefficient is 3.0, yield increases by 3 bushels/acre for each additional inch of rain, assuming temperature, nitrogen, etc. stay the same.
   </details>

3. **When would you use logistic regression instead of linear regression?**
   <details>
   <summary>Click to check</summary>
   Use logistic regression when your outcome is binary (yes/no, success/fail, 0/1). Examples: Will it rain? Will the crop fail? Is the plant diseased? Linear regression is for continuous numeric outcomes (yield, temperature, price).
   </details>

4. **Why is accuracy sometimes misleading for classification models?**
   <details>
   <summary>Click to check</summary>
   With imbalanced classes, high accuracy can be achieved by always predicting the majority class. Example: If only 2% of plants have disease, predicting "no disease" for everyone gives 98% accuracy but catches zero disease cases. Precision, recall, and AUC are often more informative.
   </details>

5. **What's the difference between correlation and causation?**
   <details>
   <summary>Click to check</summary>
   Correlation means two variables change together (when one goes up, the other tends to go up/down). Causation means one variable directly causes changes in the other. Correlation doesn't prove causation - there might be a third variable affecting both, or the relationship might be coincidental.
   </details>

### Can you do...?

1. **Fit a multiple regression model with at least 3 predictors and interpret the coefficients?**
   ```python
   # Try with this data: predict yield from rainfall, temp, nitrogen
   # Check python_notebooks/Correlation&MLR.ipynb for examples
   ```

2. **Calculate R² and MSE for a model and explain what they mean?**
   ```python
   from sklearn.metrics import r2_score, mean_squared_error
   # Practice with actual vs predicted values
   ```

3. **Fit a logistic regression model and interpret the predicted probabilities?**
   ```python
   # Try predicting a binary outcome
   # Check python_notebooks/LogisticRegression.ipynb
   ```

4. **Create and interpret a confusion matrix?**
   ```python
   from sklearn.metrics import confusion_matrix
   # What do TP, TN, FP, FN mean in your specific problem?
   ```

### Self-Check Exercises

Work through these notebooks:

- [ ] Complete the multiple regression examples in `MultipleRegression.ipynb`
- [ ] Understand the matrix formulation and try computing β manually
- [ ] Work through all logistic regression examples in `LogisticRegression.ipynb`
- [ ] Practice interpreting confusion matrices and ROC curves
- [ ] Explore the historical Galton example in `GaltonSeeds.ipynb`

### Ready for Next Module?

Check off each item:

- [ ] I can fit and interpret multiple regression models
- [ ] I understand what the normal equation does
- [ ] I can apply logistic regression to binary classification problems
- [ ] I know how to evaluate regression models (R², MSE)
- [ ] I know how to evaluate classification models (accuracy, precision, recall, AUC)
- [ ] I understand the difference between correlation and causation
- [ ] I can interpret model coefficients correctly

**All checked?** Great! Move on to [Module 03: Geospatial Fundamentals](Module_03_Geospatial_Fundamentals.md)

**Need more practice?** Focus on the areas where you're less confident. These concepts are crucial for everything that follows.

---

## Common Mistakes to Avoid

1. **Interpreting coefficients without "holding other variables constant"**
   - Wrong: "Rainfall coefficient is 3, so more rain means higher yield"
   - Right: "Holding temperature and nitrogen constant, each inch of rain adds 3 bushels/acre"

2. **Using linear regression for yes/no outcomes**
   - Linear regression can predict values outside 0-1, which doesn't make sense for probabilities
   - Always use logistic regression for binary outcomes

3. **Trusting high accuracy without checking other metrics**
   - Always look at precision, recall, and confusion matrix too
   - Especially important with imbalanced data

4. **Assuming correlation means causation**
   - Regression finds associations, not causal relationships
   - Need experiments to establish causation

5. **Not checking assumptions**
   - Regression assumes linear relationships, normal residuals, constant variance
   - Check diagnostics (GoF.ipynb) to verify assumptions hold

---

## Tips for Success

1. **Visualize your data first**: Before fitting any model, plot your predictors vs outcome. See if relationships look linear.

2. **Start simple**: Fit a model with one predictor first, then add more one at a time. See how R² and coefficients change.

3. **Check residuals**: Plot predicted vs actual, and look at residual plots. Patterns in residuals suggest model problems.

4. **Use domain knowledge**: Do the coefficients make sense? If temperature coefficient is negative for crop yield, does that align with what you know about crops?

5. **Compare models**: Fit multiple versions and compare metrics. Which predictors actually help?

6. **Cross-validate**: Test your model on held-out data to see if it generalizes (you'll learn more about this in later modules).

---

## Next Steps

Ready for spatial data?

→ **Continue to [Module 03: Geospatial Fundamentals](Module_03_Geospatial_Fundamentals.md)**

You'll learn:
- What makes spatial data special
- Coordinate reference systems
- Rasters vs vectors
- Spatial interpolation (Kriging)

---

*Statistical foundations are the bedrock of data analysis. Master these concepts and you'll be well-prepared for the spatial challenges ahead!*
