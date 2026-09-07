# Module 09: Analysis of Variance (ANOVA)

**Difficulty**: ⭐⭐ Intermediate
**Time Estimate**: 4-6 hours
**Prerequisites**: Module 02 (Regression, Hypothesis Testing)

---

## Module Overview

In previous modules, you learned how to compare two groups using t-tests (e.g., is crop yield from Seed A different from Seed B?). But what if you have **three or more** groups? 

**Analysis of Variance (ANOVA)** is the statistical method used to compare the means of three or more groups to see if they are significantly different.

### What You'll Learn
-   **One-Way ANOVA**: Comparing groups based on one factor (e.g., 3 different fertilizer types).
-   **Two-Way ANOVA**: Comparing groups based on two factors (e.g., fertilizer type AND watering schedule) and checking for interactions.
-   **The Math Behind ANOVA**: Understanding Sum of Squares (SS), Mean Squares (MS), and the F-statistic.
-   **Assumptions Checklist**: What to check before, during, and after analysis.

### Why We Need ANOVA
Why not just run multiple t-tests?
-   **Type I Error Inflation**: If you compare 3 groups (A vs B, B vs C, A vs C) with $\alpha=0.05$ each, your overall chance of making a false positive error increases to roughly $1 - (0.95)^3 \approx 14\%$.
-   ANOVA performs a single omnibus test to control this error rate.

---

## Core Concepts

### 1. One-Way ANOVA
**Definition**: A statistical test acting on a single independent variable (factor) with 3 or more levels (groups) and one continuous dependent variable.

**Hypotheses**:
-   $H_0$: $\mu_1 = \mu_2 = \dots = \mu_k$ (All group means are equal)
-   $H_1$: At least one group mean is different from the others.

**How it Works**:
ANOVA splits the total variation in the data into two parts:
1.  **Between-Group Variation**: Differences caused by the specific treatment/group.
2.  **Within-Group Variation**: Random error or natural noise within each group.

If the **Between** variation is much larger than the **Within** variation, we conclude the groups are likely different.

#### Calculations (The ANOVA Table)

| Source | Sum of Squares (SS) | Degrees of Freedom (df) | Mean Square (MS) | F-Ratio |
| :--- | :--- | :--- | :--- | :--- |
| **Between** | $SS_B$ | $k - 1$ | $MS_B = SS_B / df_B$ | $F = MS_B / MS_W$ |
| **Within (Error)** | $SS_W$ | $N - k$ | $MS_W = SS_W / df_W$ | |
| **Total** | $SS_T$ | $N - 1$ | | |

*Where $N$ is total sample size and $k$ is number of groups.*

**Step-by-Step Calculation Guide**:
1.  **Calculate Grand Mean ($\bar{X}_{GM}$)**: The average of ALL data points.
2.  **Calculate $SS_{Total}$**: Sum of squared differences between every point and the Grand Mean.
    $$SS_{total} = \sum (X_{ij} - \bar{X}_{GM})^2$$
3.  **Calculate $SS_{Between}$**: Sum of squared differences between *Group Means* and Grand Mean, weighted by group size ($n_i$).
    $$SS_{Between} = \sum n_i (\bar{X}_i - \bar{X}_{GM})^2$$
4.  **Calculate $SS_{Within}$**: Sum of squared differences between each point and its *own* Group Mean.
    $$SS_{Within} = \sum (X_{ij} - \bar{X}_i)^2$$
    *(Check: $SS_{Total} = SS_{Between} + SS_{Within}$)*
5.  **Calculate MS**: Divide SS by respective df.
6.  **Calculate F**: $F = MS_{Between} / MS_{Within}$.
7.  **Find P-value**: Use F-table with $df_1 = k-1$ and $df_2 = N-k$.

#### Python Example: One-Way ANOVA
```python
import scipy.stats as stats

# Data: Yields for 3 different fertilizers
group1 = [20, 21, 19, 22, 20]
group2 = [28, 30, 29, 28, 27]
group3 = [18, 20, 22, 19, 21]

f_stat, p_value = stats.f_oneway(group1, group2, group3)

printValues = f"F-statistic: {f_stat:.2f}, P-value: {p_value:.4f}"
print(printValues)
# If p < 0.05, we reject H0.
```

---

### 2. Two-Way ANOVA
**Definition**: Examines the effect of **two** independent categorical variables (factors) on a continuous dependent variable.

**What it adds**:
1.  **Main Effect of Factor A**: Does Factor A allow significant differences?
2.  **Main Effect of Factor B**: Does Factor B allow significant differences?
3.  **Interaction Effect (A × B)**: Does the effect of Factor A depend on the level of Factor B? (e.g., Does fertilizer only work well if there is high irrigation?)

**Calculations**:
You calculate $SS_{Total}$, $SS_A$, $SS_B$, $SS_{A \times B}$, and $SS_{Error}$.

**Differences Summary**:

| Feature | One-Way ANOVA | Two-Way ANOVA |
| :--- | :--- | :--- |
| **Independent Vars** | 1 (e.g., Fertilizer) | 2 (e.g., Fertilizer & Irrigation) |
| **Dependent Vars** | 1 (Continuous) | 1 (Continuous) |
| **Effects Tested** | Group differences | Effect of A, Effect of B, Interaction of A & B |
| **Complexity** | Simple | Moderate |

#### Python Example: Two-Way ANOVA
```python
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# DataFrame setup
df = pd.DataFrame({
    'Yield': [50, 52, 60, 62, 45, 48, 80, 85],
    'Fertilizer': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
    'Water': ['Low', 'Low', 'High', 'High', 'Low', 'Low', 'High', 'High']
})

# Fit model
model = ols('Yield ~ C(Fertilizer) + C(Water) + C(Fertilizer):C(Water)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

---

## The Ultimate ANOVA Checklist

Use this checklist for every analysis to ensure robustness.

### ✅ Phase 1: Pre-Analysis Assumptions
Before running one line of code, verify these:
- [ ] **Independence**: Observations must be independent. (Random sampling? No spatial autocorrelation?)
- [ ] **Normality**: Data within each group should be roughly normally distributed.
    -   *Test*: Shapiro-Wilk test or Histogram/Q-Q plot.
    -   *Code*: `stats.shapiro(data)`
- [ ] **Homogeneity of Variance (Homoscedasticity)**: The variance (spread) across groups should be similar.
    -   *Test*: Levene’s Test (robust to non-normality) or Bartlett’s Test (if normal).
    -   *Code*: `stats.levene(group1, group2, group3)`

### ✅ Phase 2: Execution Checks
- [ ] **Balanced Design**: Do you have roughly equal sample sizes ($N$) in groups? (ANOVA is robust to some assumption violations if $N$ is balanced).
- [ ] **Correct Data Types**: Factors should be categorical; Response should be continuous.

### ✅ Phase 3: Post-Analysis & Diagnostics
- [ ] **P-value Interpretation**:
    -   If $p < 0.05$: Reject $H_0$ (Significant difference exists).
    -   If $p \ge 0.05$: Fail to reject $H_0$.
- [ ] **Effect Size**: Calculate $\eta^2$ (Eta-squared) to know *how much* variance is explained. $\eta^2 = SS_{Between} / SS_{Total}$.
- [ ] **Post-Hoc Testing**: If ANOVA is significant, specificy *which* groups differ.
    -   *Test*: Tukey's HSD (Honest Significant Difference).
    -   *Code*: `statsmodels.stats.multicomp.pairwise_tukeyhsd`.
- [ ] **Residual Analysis**: Plot residuals vs. fitted values. There should be no pattern (random cloud). 

---

## Detailed Step-by-Step Study Guide

**Scenario**: We want to test if three varying temperatures (Low, Med, High) affect maize height.

**Step 1: Check Assumptions**
-   Is data independent? Yes, random plants.
-   Run Levene’s test on the 3 groups. If $p > 0.05$, variance is equal. Proceed.

**Step 2: Hypotheses**
-   $H_0$: $\mu_{low} = \mu_{med} = \mu_{high}$
-   $H_1$: At least one mean differs.

**Step 3: Calculate SS (Sum of Squares)**
-   Find Grand Mean.
-   Find Group Means.
-   Calculate $SS_{Total}$, $SS_{Between}$, $SS_{Within}$.

**Step 4: Degrees of Freedom**
-   $df_{between} = 3 - 1 = 2$
-   $df_{within} = 30 - 3 = 27$ (assuming $N=30$)

**Step 5: Mean Squares (MS)**
-   $MS_{Between} = SS_{Between} / 2$
-   $MS_{Within} = SS_{Within} / 27$

**Step 6: F-Statistic**
-   $F = MS_{Between} / MS_{Within}$ (e.g., $F = 4.5$)

**Step 7: Conclusion**
-   Look up critical F value for $df(2, 27)$ at $\alpha=0.05$ (approx 3.35).
-   Since $4.5 > 3.35$, we **Reject Null**.
-   **Conclusion**: Temperature significantly affects maize height.

**Step 8: Post-Hoc**
-   Run Tukey's test to see *where* the difference is (e.g., High is different from Low, but Med is same as Low).

---

## Review Questions

1.  **Why can't we just run 3 t-tests instead of one ANOVA?**
    *Answer: It increases the Type I error rate (false positives).*
    
2.  **What does a significant Interaction term in Two-Way ANOVA mean?**
    *Answer: It means the effect of one factor depends on the level of the other factor (e.g., Fertilizer increases yield ONLY when water is high).*

3.  **What is the most important assumption to check for ANOVA?**
    *Answer: Homogeneity of variance (Levene's test).*
