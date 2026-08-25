# Module 01: Foundations
## Python Basics, Statistics & Visualization

**Difficulty**: ⭐ Beginner
**Time Estimate**: 3-5 hours
**Prerequisites**: None - This is your starting point!

---

## Module Overview

This module introduces you to Python programming and basic statistical concepts. Think of this as building your toolbox - you'll learn the fundamental tools you'll use throughout the course.

### What You'll Learn
- How to store and organize data in Python
- How to make decisions and repeat actions in your code
- How to visualize data with charts and graphs
- Basic statistical measures (mean, standard deviation, etc.)
- How different types of data are distributed
- Simple linear regression (finding the line of best fit)

### Why This Matters
Before you can analyze spatial data or build complex models, you need to understand how to:
- Work with data in Python
- Calculate basic statistics
- Visualize patterns
- Understand relationships between variables

---

## Learning Objectives

By the end of this module, you will be able to:
- [ ] Create and manipulate Python data structures (lists, dictionaries, tuples)
- [ ] Write functions and use control flow (if/else, loops)
- [ ] Create visualizations using Plotly
- [ ] Calculate summary statistics (mean, median, standard deviation)
- [ ] Understand common probability distributions
- [ ] Fit a simple linear regression model
- [ ] Interpret Q-Q plots for normality

---

## Core Concepts

### 1. Python Data Types

#### Lists
**What it is**: Think of a list like a shopping cart - it's a container that holds multiple items in order.

```python
# A list of temperatures
temperatures = [72, 75, 68, 80, 77]

# Access the first item (Python starts counting at 0!)
first_temp = temperatures[0]  # Returns 72

# Add a new temperature
temperatures.append(79)
```

**Why it matters**: Lists let you store multiple measurements (like daily temperatures or crop yields) and work with them all at once.

#### Dictionaries
**What it is**: Think of a dictionary like a real dictionary - you look up a word (the "key") to find its definition (the "value").

```python
# A dictionary storing field information
field_info = {
    "area": 100,  # acres
    "crop": "corn",
    "yield": 180  # bushels per acre
}

# Access a value using its key
crop_type = field_info["crop"]  # Returns "corn"
```

**Why it matters**: Dictionaries help you organize related information together, like keeping all data about a field in one place.

#### Tuples
**What it is**: Like a list, but it can't be changed once created. Think of it as a sealed package.

```python
# GPS coordinates (latitude, longitude) - shouldn't change!
location = (40.1106, -88.2073)
```

**Why it matters**: Use tuples for data that shouldn't be modified, like coordinates or fixed parameters.

---

### 2. Control Flow

#### If/Else Statements
**What it is**: Making decisions in your code, like choosing a path at a fork in the road.

```python
temperature = 75

if temperature > 80:
    print("It's hot!")
elif temperature > 60:
    print("It's comfortable")
else:
    print("It's cold!")
```

**Simple example**: Imagine you're deciding whether to irrigate a field:
```python
soil_moisture = 15  # percent

if soil_moisture < 20:
    action = "Irrigate immediately"
elif soil_moisture < 35:
    action = "Monitor closely"
else:
    action = "No irrigation needed"
```

#### Loops
**What it is**: Repeating an action multiple times, like checking each plant in a row.

```python
# For loop - repeat a fixed number of times
yields = [180, 175, 190, 165, 185]

for yield_value in yields:
    print(f"This field produced {yield_value} bushels/acre")

# While loop - repeat until a condition is met
water_level = 100
day = 0

while water_level > 20:
    water_level = water_level - 5  # Decrease by 5% per day
    day = day + 1

print(f"Need to refill after {day} days")
```

#### List Comprehension
**What it is**: A compact way to create a new list by transforming each item in an existing list.

```python
# Convert Fahrenheit to Celsius for all temperatures
fahrenheit = [72, 75, 68, 80, 77]
celsius = [(temp - 32) * 5/9 for temp in fahrenheit]

# Result: [22.2, 23.9, 20.0, 26.7, 25.0]
```

Think of it as an assembly line - each item goes in, gets transformed, and comes out changed.

---

### 3. Functions

**What it is**: A reusable recipe for a task. Write it once, use it many times.

```python
def calculate_yield(area, production):
    """Calculate yield per acre"""
    return production / area

# Use the function
field1_yield = calculate_yield(100, 18000)  # 180 bushels/acre
field2_yield = calculate_yield(150, 26250)  # 175 bushels/acre
```

**Why it matters**: Functions help you:
- Avoid repeating the same code
- Make your code easier to understand
- Reduce mistakes (fix it once, it's fixed everywhere)

**Simple example**: A function to categorize crop yields:
```python
def yield_category(yield_value):
    """Categorize yield as low, medium, or high"""
    if yield_value < 150:
        return "Low"
    elif yield_value < 180:
        return "Medium"
    else:
        return "High"

# Use it
print(yield_category(165))  # Returns "Medium"
print(yield_category(190))  # Returns "High"
```

---

### 4. Visualization with Plotly

**What it is**: Creating charts and graphs to see patterns in your data that numbers alone might hide.

**Why it matters**: A good chart can show you in seconds what might take hours to understand from tables of numbers.

**Common plot types**:

1. **Scatter plot**: Shows the relationship between two variables
   - Example: Plot yield vs rainfall to see if more rain means higher yield

2. **Histogram**: Shows how data is distributed
   - Example: How many fields produced 150-160 bushels/acre? 160-170?

3. **Line plot**: Shows how something changes over time
   - Example: Daily temperature over a growing season

**Simple example**: Imagine plotting crop yield vs fertilizer amount to see if more fertilizer helps:
```python
import plotly.graph_objects as go

fertilizer = [0, 50, 100, 150, 200]  # pounds per acre
yield_data = [120, 150, 175, 180, 181]  # bushels per acre

fig = go.Figure(data=go.Scatter(x=fertilizer, y=yield_data, mode='markers'))
fig.update_layout(title='Yield vs Fertilizer',
                  xaxis_title='Fertilizer (lbs/acre)',
                  yaxis_title='Yield (bushels/acre)')
fig.show()
```

---

### 5. Summary Statistics

**What it is**: Single numbers that describe your entire dataset.

#### Mean (Average)
**Simple explanation**: Add up all the values and divide by how many you have.

```python
yields = [180, 175, 190, 165, 185]
mean_yield = sum(yields) / len(yields)  # 179
```

**Why it matters**: Gives you a "typical" value, but can be misleading if you have outliers.

#### Median (Middle Value)
**Simple explanation**: Line up all values from smallest to largest and pick the middle one.

```python
import numpy as np
yields = [180, 175, 190, 165, 185]
median_yield = np.median(yields)  # 180
```

**Example**: If yields are [100, 175, 180, 185, 190], the median is 180 (the middle value). If one field had a terrible year and only produced 10 bushels, the mean would drop a lot, but the median would barely change. That's why median is often more reliable!

#### Standard Deviation
**Simple explanation**: Measures how spread out your data is. Small standard deviation = most values are close to the mean. Large standard deviation = values are all over the place.

```python
import numpy as np
yields = [180, 175, 190, 165, 185]
std_dev = np.std(yields)  # About 9.1
```

**Think of it this way**:
- Standard deviation of 5: Most fields produce within 5 bushels of the average (very consistent!)
- Standard deviation of 30: Yields vary wildly (inconsistent - might need to investigate why!)

---

### 6. Probability Distributions

**What it is**: A pattern that describes how likely different values are to occur.

#### Normal Distribution (Bell Curve)
**Simple explanation**: Most values cluster around the average, with fewer values as you go further away. Looks like a bell when plotted.

**Real-world example**: Heights of corn plants in a field. Most are around average height (say, 8 feet), some are a bit shorter (7 feet) or taller (9 feet), and very few are extremely short (5 feet) or tall (11 feet).

**In Python**:
```python
from scipy import stats
import numpy as np

# Generate 1000 random values from a normal distribution
# mean=170, standard deviation=15
yields = stats.norm.rvs(loc=170, scale=15, size=1000)
```

#### Binomial Distribution
**Simple explanation**: Used when you have yes/no outcomes repeated many times.

**Real-world example**: Germination test. If 85% of seeds normally germinate, what's the probability that exactly 80 out of 100 seeds will germinate?

```python
from scipy import stats

# Probability of exactly 80 successes in 100 trials with 85% success rate
prob = stats.binom.pmf(k=80, n=100, p=0.85)
```

#### Poisson Distribution
**Simple explanation**: Used for counting how many times something happens in a fixed period.

**Real-world example**: Number of weeds found per square meter in a field. Average is 5 weeds/m². What's the probability of finding exactly 3 weeds in a random square meter?

```python
from scipy import stats

# Probability of exactly 3 occurrences when average is 5
prob = stats.poisson.pmf(k=3, mu=5)
```

---

### 7. Simple Linear Regression

**What it is**: Finding the straight line that best fits through a scatter of points. Used to predict one variable based on another.

**Simple explanation**: Imagine you have crop yield data and rainfall data for many fields. Linear regression finds the line that best shows how yield changes with rainfall. Then you can use that line to predict: "If we get 30 inches of rain, what yield should we expect?"

**The equation**: `y = mx + b`
- `y` = what you're predicting (yield)
- `x` = what you know (rainfall)
- `m` = slope (how much y changes when x increases by 1)
- `b` = intercept (value of y when x is 0)

**Real example**:
```python
import numpy as np
from scipy import stats

# Rainfall data (inches)
rainfall = np.array([20, 25, 30, 35, 40])

# Yield data (bushels/acre)
yields = np.array([140, 160, 175, 185, 190])

# Fit the line
slope, intercept, r_value, p_value, std_err = stats.linregress(rainfall, yields)

# Predict yield for 32 inches of rainfall
predicted_yield = slope * 32 + intercept

print(f"For 32 inches of rain, expect {predicted_yield:.1f} bushels/acre")
print(f"R-squared: {r_value**2:.3f}")  # How well the line fits (0-1, higher is better)
```

**Understanding R-squared**:
- R² = 0.95: The line fits the data really well (95% of variation in yield is explained by rainfall)
- R² = 0.50: The line fits okay (rainfall explains 50% of yield variation)
- R² = 0.10: The line fits poorly (rainfall barely explains yield variation)

---

### 8. Q-Q Plots (Quantile-Quantile Plots)

**What it is**: A visual way to check if your data follows a normal distribution.

**Simple explanation**: A Q-Q plot compares your data to what you'd expect if it were perfectly normally distributed. If the points fall on a straight diagonal line, your data is normal. If they curve or scatter, it's not.

**Why it matters**: Many statistical tests assume your data is normally distributed. A Q-Q plot helps you check this assumption.

**How to read it**:
- Points on the diagonal line = data is normal
- Points curve upward at the ends = data has more extreme values than normal (heavy tails)
- Points curve downward = data has fewer extreme values than normal
- Points form an S-shape = data is skewed

**Simple example**: You measure soil nitrogen levels in 100 locations. Before running certain analyses, you check if the data is normally distributed:

```python
import scipy.stats as stats
import matplotlib.pyplot as plt

# Your data
nitrogen_levels = [45, 48, 50, 52, 47, 49, 51, ...]  # 100 measurements

# Create Q-Q plot
stats.probplot(nitrogen_levels, dist="norm", plot=plt)
plt.title("Q-Q Plot: Nitrogen Levels")
plt.show()
```

If the points fall on the line, your nitrogen data is normally distributed and you can proceed with analyses that assume normality!

---

## Course Materials

### Primary Notebooks

1. **[python_cheat_sheet.ipynb](/tmp/cpsc444-study/python_cheat_sheet.ipynb)**
   - Comprehensive Python reference
   - Data types, control flow, functions
   - Plotly visualization examples
   - Your main reference document!

2. **[w01-exercises/Colab+Python-warmUp.ipynb](/tmp/cpsc444-study/w01-exercises/Colab+Python-warmUp.ipynb)**
   - Python warm-up exercises
   - Regression simulation example
   - Hands-on practice with basic concepts

3. **[w01-exercises/Basic_Functions_python.ipynb](/tmp/cpsc444-study/w01-exercises/Basic_Functions_python.ipynb)**
   - Statistical functions in Python
   - Distribution functions (binomial, normal, Poisson, etc.)
   - Practical examples

### Reference Materials

4. **[old_cheatsheet.ipynb](/tmp/cpsc444-study/old_cheatsheet.ipynb)**
   - Alternative reference with additional examples
   - Different perspective on core concepts

---

## Key Formulas

### Mean
```
mean = (x₁ + x₂ + x₃ + ... + xₙ) / n
```
**In words**: Add all values, divide by how many there are.

### Standard Deviation
```
σ = √[Σ(xᵢ - mean)² / n]
```
**In words**:
1. Subtract the mean from each value
2. Square each result
3. Find the average of those squares
4. Take the square root

### Linear Regression Slope
```
m = Σ[(xᵢ - x̄)(yᵢ - ȳ)] / Σ[(xᵢ - x̄)²]
```
**In words**: The slope tells you how much y changes when x increases by 1.

### Linear Regression Intercept
```
b = ȳ - m·x̄
```
**In words**: The intercept is where the line crosses the y-axis (value of y when x=0).

---

## Study Checkpoints

Before moving to Module 02, make sure you can answer these questions:

### Can you explain...?

1. **What's the difference between a list and a dictionary in Python?**
   <details>
   <summary>Click to check your understanding</summary>
   A list stores items in order and you access them by position (index). A dictionary stores key-value pairs and you access values using their keys. Lists are like a numbered shopping list; dictionaries are like a phone book (name → number).
   </details>

2. **When would you use a for loop vs a while loop?**
   <details>
   <summary>Click to check your understanding</summary>
   Use a for loop when you know how many times to repeat (like processing each item in a list). Use a while loop when you repeat until a condition is met (like "keep adding water until the tank is full").
   </details>

3. **What does standard deviation tell you about your data?**
   <details>
   <summary>Click to check your understanding</summary>
   Standard deviation measures spread. Low = data points are close to the mean (consistent). High = data points are scattered (variable). Example: std dev of 5 means most values are within 5 units of the mean.
   </details>

4. **What's the difference between mean and median?**
   <details>
   <summary>Click to check your understanding</summary>
   Mean = average (sum ÷ count). Median = middle value when sorted. Median is better when you have outliers because it's not affected by extreme values like mean is.
   </details>

5. **What does R-squared tell you in a regression?**
   <details>
   <summary>Click to check your understanding</summary>
   R² tells you how well your line fits the data. R²=0.9 means 90% of the variation in y is explained by x (good fit). R²=0.2 means only 20% is explained (poor fit). Range: 0 to 1, higher is better.
   </details>

### Can you do...?

1. **Create a list of numbers and calculate their mean using Python?**
   ```python
   # Try it yourself first, then check:
   data = [10, 15, 12, 18, 14]
   mean = sum(data) / len(data)
   # Or using numpy: mean = np.mean(data)
   ```

2. **Write a function that takes a temperature in Fahrenheit and returns Celsius?**
   ```python
   # Formula: C = (F - 32) × 5/9
   # Try writing it, then check:
   def f_to_c(fahrenheit):
       return (fahrenheit - 32) * 5/9
   ```

3. **Use list comprehension to square every number in a list?**
   ```python
   # If you have [1, 2, 3, 4, 5], create [1, 4, 9, 16, 25]
   # Try it, then check:
   numbers = [1, 2, 3, 4, 5]
   squared = [n**2 for n in numbers]
   ```

4. **Create a simple scatter plot showing the relationship between two variables?**
   ```python
   # Try using Plotly to plot hours studied vs test score
   # Check the python_cheat_sheet.ipynb for examples
   ```

### Self-Check Exercises

Work through these notebooks and make sure you understand them:

- [ ] Complete the warm-up exercises in `Colab+Python-warmUp.ipynb`
- [ ] Run all examples in `python_cheat_sheet.ipynb` and modify them
- [ ] Practice with distributions in `Basic_Functions_python.ipynb`
- [ ] Create your own simple linear regression with made-up data

### Ready for Next Module?

Check off each item:

- [ ] I can create and manipulate lists, dictionaries, and tuples
- [ ] I can write if/else statements and loops
- [ ] I can write and use functions
- [ ] I understand mean, median, and standard deviation
- [ ] I can explain what a normal distribution is
- [ ] I can fit a simple linear regression and interpret R²
- [ ] I can create basic visualizations with Plotly or Matplotlib

**If you checked all items**: Congratulations! You're ready for [Module 02: Statistical Foundations](Module_02_Statistical_Foundations.md)

**If you're unsure about some items**: That's okay! Review the relevant sections and work through the notebooks again. These are foundational skills you'll use throughout the course.

---

## Learning Tips for This Module

1. **Type, don't copy-paste**: You learn by doing. Type out the code examples yourself.

2. **Break things intentionally**: Change values, try different inputs, see what happens when things go wrong. This builds understanding.

3. **Use print() liberally**: When learning, print intermediate values to see what's happening at each step.

4. **Start simple**: If an example is complex, create a simpler version first. Master that, then add complexity.

5. **Relate to the real world**: Every concept has a real-world application. Think about how you'd use it with actual data.

6. **Don't memorize syntax**: You'll remember it through use. It's okay to look things up!

7. **Practice with your own data**: If you have data from a project or hobby, try applying these concepts to it.

---

## Common Beginner Mistakes

1. **Forgetting that Python starts counting at 0**
   ```python
   temps = [72, 75, 68]
   first_temp = temps[0]  # Not temps[1]!
   ```

2. **Confusing = and ==**
   - `=` assigns a value: `x = 5`
   - `==` checks if equal: `if x == 5:`

3. **Indentation errors**
   Python uses indentation to group code. All lines in a function or loop must be indented the same way.

4. **Forgetting to import libraries**
   ```python
   import numpy as np  # Do this at the top of your file!
   mean = np.mean(data)  # Now you can use numpy
   ```

5. **Interpreting correlation as causation**
   Just because yield and rainfall are correlated doesn't mean rain directly causes yield changes. Other factors might be involved!

---

## Next Steps

Once you're comfortable with this module:

→ **Continue to [Module 02: Statistical Foundations](Module_02_Statistical_Foundations.md)**

You'll learn about:
- Multiple regression (predicting with multiple variables)
- Logistic regression (yes/no predictions)
- Model evaluation techniques
- Correlation analysis

---

*Remember: Everyone learns at their own pace. Take your time, practice, and don't hesitate to revisit concepts that seem unclear!*
