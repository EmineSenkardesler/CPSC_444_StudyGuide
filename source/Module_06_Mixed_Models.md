# Module 06: Mixed Models & Hierarchical Data
## Fixed vs Random Effects, BLUP & EM Algorithm

**Difficulty**: ⭐⭐⭐⭐⭐ Advanced
**Time Estimate**: 10-12 hours
**Prerequisites**: Modules 02 (Regression), 04 (Spatial stats)

---

## Module Overview

Regular regression assumes all observations are independent. But what if your data has GROUPS? Like plots within fields, fields within farms, students within schools? Mixed models handle hierarchical (nested) data properly.

### What You'll Learn
- Fixed vs random effects
- Random intercept and random slope models
- Best Linear Unbiased Prediction (BLUP)
- Expectation-Maximization (EM) algorithm
- When to use mixed models vs regular regression

### Why This Matters
Agricultural and environmental data is often hierarchical:
- Measurements within plots within fields
- Fields within farms within regions
- Time series within locations
- Ignoring this structure leads to wrong conclusions!

---

## Core Concepts

### 1. The Hierarchical Data Problem

**Example**: Measuring crop yield in a multi-location trial

```
Farm 1:
  Field A: [180, 175, 182, 178]
  Field B: [165, 170, 168, 172]

Farm 2:
  Field C: [190, 185, 192, 188]
  Field D: [175, 178, 173, 180]
```

**Problem with regular regression**:
- Treats all 16 measurements as independent
- **But they're not!** Measurements within the same field are more similar

**Why it matters**:
- Underestimates uncertainty
- Incorrect p-values
- Wrong conclusions about treatment effects

**Solution**: Mixed models account for grouping

---

### 2. Fixed vs Random Effects

**Fixed effects**: Variables you want to estimate and make inferences about
- Treatment effects (fertilizer amount, variety)
- Controlled experimental factors
- **Example**: Effect of nitrogen level on yield

**Random effects**: Random variation due to grouping
- Field-to-field variation
- Farm-to-farm variation
- Not interested in specific values, just the variability
- **Example**: Which farm doesn't matter, but farms vary randomly

**Simple analogy**:
- **Fixed**: You specifically chose these treatments to test
- **Random**: You randomly sampled these fields/farms from a larger population

**Mathematical notation**:
```
Fixed effect: y = β₀ + β₁ × treatment + ε
Random effect: y = β₀ + u_j + β₁ × treatment + ε
                      ↑
             random intercept for group j
```

---

### 3. Random Intercept Model

**The idea**: Each group has its own baseline (intercept), but same slope.

**Example**: Yield vs fertilizer across multiple fields

**Model**:
```
y_ij = (β₀ + u_j) + β₁ × fertilizer + ε_ij
       ↑
   intercept for field j
```

**Simple explanation**:
- `β₀`: Average baseline yield (fixed)
- `u_j`: How much field j differs from average (random)
- `β₁`: Fertilizer effect (fixed, same for all fields)
- `ε_ij`: Residual error

**Visual**:
```
Yield
  |     Field C ___/
  |         /
  |    Field A___/     All parallel (same slope β₁)
  |       /
  | Field B___/      But different intercepts
  |
  +-------------------> Fertilizer
```

**When to use**: Groups have different baselines but same response to predictors

**Python (using statsmodels)**:
```python
import statsmodels.formula.api as smf

# Random intercept for field
model = smf.mixedlm(
    "yield ~ fertilizer",  # Fixed effects
    data,
    groups=data["field_id"]  # Random intercept per field
)
result = model.fit()
print(result.summary())
```

---

### 4. Random Slope Model

**The idea**: Each group has different baseline AND different response to predictors.

**Model**:
```
y_ij = (β₀ + u_0j) + (β₁ + u_1j) × fertilizer + ε_ij
                      ↑
               random slope for field j
```

**Visual**:
```
Yield
  |       ___/  Field C (high baseline, strong response)
  |    __/
  | __/ Field A (medium)
  |_____
  |     ---  Field B (low baseline, weak response)
  +-------------------> Fertilizer
```

**When to use**: Both baseline and response vary by group

**Example**: Fertilizer response differs by soil type - sandy soils respond differently than clay soils.

**Python**:
```python
# Random intercept AND random slope
model = smf.mixedlm(
    "yield ~ fertilizer",
    data,
    groups=data["field_id"],
    re_formula="~fertilizer"  # Random slope on fertilizer
)
result = model.fit()
```

---

### 5. BLUP (Best Linear Unbiased Prediction)

**What it is**: Method for predicting random effects.

**Simple explanation**: BLUP "shrinks" group-specific estimates toward the global average. Groups with little data get shrunk more.

**Example**: Estimating yield for each field

**Naive approach**: Average yield in each field
- Field with 100 observations: Trust the average
- Field with 2 observations: Don't trust the average (too noisy!)

**BLUP approach**:
- Field with lots of data: Estimate close to field average
- Field with little data: Shrink toward overall average

**Formula (conceptual)**:
```
BLUP_j = w × field_j_average + (1-w) × global_average

where w depends on:
  - Amount of data in group
  - Within-group variability
  - Between-group variability
```

**Why it's better**: Prevents overconfidence in noisy estimates

---

### 6. Variance Components

**Mixed models partition variance**:

```
Total variance = Between-group variance + Within-group variance

σ²_total = σ²_between + σ²_within
```

**Example**:
- Total yield variance: 400 (bushels/acre)²
- Between-field variance: 250
- Within-field variance: 150

**Interpretation**: 62.5% of variation is between fields, 37.5% within fields

**Intraclass Correlation (ICC)**:
```
ICC = σ²_between / (σ²_between + σ²_within)
    = 250 / 400
    = 0.625
```

**Meaning**: 62.5% of variance is due to field differences

**Why it matters**: High ICC = must account for grouping! Low ICC = regular regression might be okay.

---

### 7. Expectation-Maximization (EM) Algorithm

**What it is**: Iterative algorithm for fitting mixed models when you have missing information (the random effects).

**The problem**: You want to estimate:
- Fixed effects (β)
- Random effects (u)
- Variance components (σ²)

But random effects aren't directly observed!

**EM Solution - Two steps repeated**:

**E-step (Expectation)**: Given current parameter estimates, predict random effects
**M-step (Maximization)**: Given random effect predictions, update parameter estimates

**Repeat until convergence**

**Conceptual algorithm**:
```
1. Initialize parameters (β, σ²_between, σ²_within)

2. Repeat until convergence:

   E-step:
   - Predict random effects u_j given current parameters
   - These are the BLUPs

   M-step:
   - Update β by weighted regression
   - Update σ² components by analyzing residuals

3. Converged parameters are final estimates
```

**Why it works**: Each step improves the likelihood. Eventually reaches optimum.

**You don't implement this yourself** - it's built into mixed model functions. But understanding it helps you:
- Know why fitting takes longer than regular regression
- Understand convergence warnings
- Interpret the output

---

### 8. Comparing Models: ANOVA vs Mixed Models

**ANOVA approach**:
- Treats groups as fixed effects
- Tests if group means differ
- Can't predict new groups

**Mixed model approach**:
- Treats groups as random sample from population
- Estimates variance components
- Can predict new groups (using BLUP)

**When to use each**:

**Use ANOVA when**:
- You care about specific groups (these exact fields)
- Not generalizing to other groups
- Small number of groups

**Use mixed models when**:
- Groups are random sample (could have been different fields)
- Want to generalize to population
- Many groups (10+)
- Unbalanced data (different sample sizes per group)

---

## Course Materials

1. **[MLM_implementation.ipynb](/tmp/cpsc444-study/python_notebooks/MLM_implementation.ipynb)**
   - Implementing mixed linear models
   - Random intercepts and slopes
   - Variance components

2. **[ANOVAvsMLM.ipynb](/tmp/cpsc444-study/python_notebooks/ANOVAvsMLM.ipynb)**
   - Comparing ANOVA and mixed models
   - When to use each
   - Interpretation differences

3. **[Part1_ANOVAvsMLM+SpatialEffects.ipynb](/tmp/cpsc444-study/python_notebooks/Part1_ANOVAvsMLM+SpatialEffects.ipynb)**
   - Adding spatial effects to mixed models
   - Combining hierarchical and spatial structure

4. **[ExpectationMaximization.ipynb](/tmp/cpsc444-study/python_notebooks/ExpectationMaximization.ipynb)**
   - EM algorithm details
   - How mixed models are fit
   - Convergence and diagnostics

---

## Key Formulas

### Random Intercept Model
```
y_ij = (β₀ + u_j) + β₁x_ij + ε_ij

where:
  u_j ~ N(0, σ²_between)
  ε_ij ~ N(0, σ²_within)
```

### Random Slope Model
```
y_ij = (β₀ + u_0j) + (β₁ + u_1j)x_ij + ε_ij
```

### Variance Decomposition
```
Var(y_ij) = σ²_between + σ²_within
```

### Intraclass Correlation
```
ICC = σ²_between / (σ²_between + σ²_within)
```

---

## Study Checkpoints

### Can you explain...?
1. **What's the difference between fixed and random effects?**
2. **Why use mixed models instead of regular regression?**
3. **What does BLUP do and why is it better than simple averages?**
4. **What does ICC tell you about your data?**

### Can you do...?
1. **Fit a random intercept model?**
2. **Interpret variance components?**
3. **Compare ANOVA vs mixed model results?**
4. **Extract and interpret BLUPs?**

### Ready?
- [ ] I understand fixed vs random effects
- [ ] I can fit random intercept/slope models
- [ ] I know when to use mixed models
- [ ] I understand BLUP and EM algorithm basics

**Next**: [Module 07: Machine Learning](Module_07_Machine_Learning.md)

---

*Mixed models are essential for real-world hierarchical data - master them and avoid common pitfalls!*
