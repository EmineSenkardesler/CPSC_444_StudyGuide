# Lesson 1 — Getting Started with Python & Google Colab

**Course:** CPSC 444 — Intro to Spatial Statistics and Analysis
**Duration:** ~75 min (adjust to your section length)
**Format:** Live-coding in Google Colab; students follow along in their own notebook

---

## Learning Objectives

By the end of this lesson, students will be able to:

1. **Explain** what Python is and why it is the language of choice for spatial statistics and data analysis (ecosystem: NumPy, pandas, matplotlib, geopandas later in the course).
2. **Set up and navigate** a Google Colab notebook: create a notebook, run code cells vs. text (Markdown) cells, restart the runtime, and save a copy to their own Google Drive.
3. **Assign and use variables**, and follow Python naming conventions (lowercase_with_underscores, descriptive names).
4. **Identify and convert between core data types**: `int`, `float`, `str`, `bool`, and containers `list` and `dict`; use `type()` to inspect them.
5. **Write conditional logic** with `if` / `elif` / `else` using comparison (`==`, `<`, `>=`) and logical operators (`and`, `or`, `not`).
6. **Write loops** (`for` over a list and over `range()`; a simple `while`) to repeat operations, and combine loops with conditionals.
7. **Create a basic plot** with `matplotlib.pyplot`: a line plot and a scatter plot with a title, axis labels, and a legend.
8. **Interpret and respond to error messages** (e.g., `NameError`, `TypeError`, `SyntaxError`) instead of panicking — read the last line first.

---

## Materials & Prep (before class)

- [ ] Post the Colab starter notebook link (view-only; students "Save a copy in Drive").
- [ ] Confirm students have Google accounts (Illinois accounts work with Colab).
- [ ] Have a backup plan: if Colab/Wi-Fi fails, demo on the projector and share the finished notebook afterward.
- [ ] Optional: a small CSV or hardcoded data list themed on spatial data (e.g., monthly temperatures, city populations) so plots feel relevant to the course.

---

## Lesson Outline

### 1. Welcome & Why Python? (5–8 min)

Talking points:
- This course = spatial statistics + hands-on analysis. Python is the tool we'll use all semester.
- Why Python: free, readable, huge scientific ecosystem. Later we'll use libraries like `numpy`, `pandas`, `matplotlib`, and `geopandas` — today is the foundation.
- No installation needed today: everything runs in the browser via Google Colab.
- Reassure: no programming background assumed. Making errors is part of the process.

### 2. Google Colab Tour (10 min) — live demo, students follow

- Go to **colab.research.google.com** → New Notebook.
- Anatomy of a notebook:
  - **Code cells** — run with Shift+Enter (or the play button).
  - **Text cells** — Markdown for notes; double-click to edit.
- First command, the classic:
  ```python
  print("Hello, CPSC 444!")
  ```
- Key survival skills:
  - Cells share memory: a variable defined in one cell is available in others — **order of execution matters**, not order on the page.
  - **Runtime → Restart runtime** wipes memory; "Restart and run all" is the clean test that a notebook works top to bottom.
  - **File → Save a copy in Drive** — do this now so your work persists.
  - Runtimes disconnect after idle time; your *code text* is saved, but *variables in memory* are lost — just re-run the cells.

> Common pitfall to demo on purpose: run cells out of order so a `NameError` appears, then fix it with Restart & Run All.

### 3. Variables & Data Types (15 min)

```python
# Assignment: name = value  (no declaration needed)
city = "Urbana"          # str
population = 38736       # int
area_km2 = 30.1          # float
is_college_town = True   # bool

print(type(city), type(population), type(area_km2), type(is_college_town))
```

- Variables are labels for values; `=` means "assign," not "equals."
- Naming rules: start with a letter, no spaces, case-sensitive; convention is `snake_case`.
- Dynamic typing: Python figures out the type; `type()` tells you what you have.
- Basic operations & a first "analysis":
  ```python
  density = population / area_km2   # people per km^2
  print("Population density:", density)
  ```
- String formatting (they'll use this constantly):
  ```python
  print(f"{city} has a density of {density:.1f} people/km²")
  ```
- Type conversion and a classic gotcha:
  ```python
  year = "2026"
  # year + 1        -> TypeError!  (show it, read the error together)
  int(year) + 1     # 2027
  ```
- Containers (just enough for today):
  ```python
  temps = [22.5, 24.1, 19.8, 21.0]      # list: ordered, indexed from 0
  temps[0]                               # first element
  len(temps)                             # how many

  city_info = {"name": "Urbana", "state": "IL", "pop": 38736}   # dict: key -> value
  city_info["pop"]
  ```

**Check for understanding (2 min exercise):** Create variables for your hometown's name and an estimate of its population; print a sentence using an f-string.

### 4. If / Elif / Else (10 min)

```python
temperature = 24.1

if temperature > 30:
    print("Hot day")
elif temperature > 20:
    print("Pleasant day")
else:
    print("Cool day")
```

- **Indentation is syntax** in Python — 4 spaces define the block. (Most common beginner error; show the `IndentationError`.)
- Comparison operators: `==` (equality — not `=`!), `!=`, `<`, `<=`, `>`, `>=`.
- Combine conditions:
  ```python
  if temperature > 20 and temperature < 30:
      print("Comfortable")
  ```
- Spatial-flavored example: classify population density.
  ```python
  if density > 1000:
      category = "urban"
  elif density > 300:
      category = "suburban"
  else:
      category = "rural"
  print(city, "is", category)
  ```

**Check for understanding:** Change the numbers so your hometown gets classified; does the category make sense?

### 5. Loops (12 min)

```python
cities = ["Urbana", "Champaign", "Chicago", "Springfield"]

for c in cities:
    print("Processing:", c)
```

- `for` visits each item once; the loop variable (`c`) takes each value in turn.
- `range()` when you need numbers:
  ```python
  for i in range(5):        # 0, 1, 2, 3, 4
      print(i, i**2)
  ```
- Accumulator pattern (the workhorse of data analysis):
  ```python
  temps = [22.5, 24.1, 19.8, 21.0]
  total = 0
  for t in temps:
      total = total + t
  mean_temp = total / len(temps)
  print("Mean temperature:", mean_temp)
  ```
  (Mention: later we'll just call `sum(temps)/len(temps)` or use NumPy — but this is what's happening underneath.)
- Loop + conditional together:
  ```python
  for t in temps:
      if t > 21:
          print(t, "is above 21°C")
  ```
- `while` briefly — loop until a condition changes:
  ```python
  count = 0
  while count < 3:
      print("count is", count)
      count = count + 1
  ```
  Warn about infinite loops; show the ⏹ stop button in Colab.

**Check for understanding:** Loop over `temps` and count how many values are below 22.

### 6. Plotting with Matplotlib (12 min)

```python
import matplotlib.pyplot as plt

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
temps  = [-3, -1, 5, 12, 18, 23, 25, 24, 20, 13, 6, -1]   # Urbana-ish monthly means

plt.plot(months, temps)
plt.title("Average Monthly Temperature, Urbana IL")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.show()
```

- `import` brings in a library; `plt` is the universal nickname for `matplotlib.pyplot`.
- Anatomy of a plot: data → `plot()` / `scatter()` → labels → `show()`.
- A plot without axis labels and a title is incomplete — this will be a grading standard all semester.
- Scatter plot + styling + legend:
  ```python
  plt.scatter(months, temps, color="red", label="2025")
  plt.plot(months, temps, linestyle="--", alpha=0.5)
  plt.title("Average Monthly Temperature, Urbana IL")
  plt.xlabel("Month")
  plt.ylabel("Temperature (°C)")
  plt.legend()
  plt.show()
  ```
- Tease the semester: "In a few weeks, the x and y will be longitude and latitude, and this scatter plot becomes a map."

**Check for understanding:** Change the color, or plot only months 6–8 (list slicing bonus: `months[5:8]`).

#### Bonus: your first raster (if time allows, or as a closer)

```python
import numpy as np
import matplotlib.pyplot as plt

# A raster is just a grid of numbers — one value per cell (like pixels)
nrows, ncols = 50, 50

# Coordinates for every cell in the grid
x = np.linspace(0, 10, ncols)
y = np.linspace(0, 10, nrows)
X, Y = np.meshgrid(x, y)

# Fill the grid with a smooth "surface" (think elevation or temperature)
# plus a little random noise so it looks like real data
elevation = 100 + 20 * np.sin(X / 2) * np.cos(Y / 3) + np.random.normal(0, 2, size=(nrows, ncols))

plt.imshow(elevation, cmap="terrain", origin="lower", extent=[0, 10, 0, 10])
plt.colorbar(label="Elevation (m)")
plt.title("A Simple Raster: Simulated Elevation Surface")
plt.xlabel("X (km)")
plt.ylabel("Y (km)")
plt.show()
```

Talking points:
- A raster is just a **2D array of numbers** — show `elevation.shape` and `elevation[0, 0]` to connect back to lists and indexing.
- `imshow()` maps numbers → colors; the **colorbar is the legend for a raster** (same "always label your plot" rule).
- `origin="lower"` puts row 0 at the bottom so it reads like a map, not an image.
- Student exercise: swap `cmap="terrain"` for `"viridis"` or `"hot"` and re-run.
- No-NumPy fallback (reinforces the loops section): build the grid with a nested loop, e.g. `grid = [[i + j for j in range(20)] for i in range(20)]`, then `plt.imshow(grid)`.

### 7. Wrap-up & Exit Ticket (5 min)

- Recap against the learning objectives (put them back on the screen; ask thumbs up/down per item).
- **Exit ticket / mini-exercise** (finish in class or as homework):
  1. Make a list of 5+ numbers (e.g., rainfall for 5 days).
  2. Use a loop to compute the mean.
  3. Use an if/else to print whether the mean is above or below some threshold.
  4. Plot the values with a title and labeled axes.
  5. Save the notebook to Drive and submit the share link.
- Preview next lesson: functions and NumPy/pandas — working with real datasets.

---

## Anticipated Questions & Pitfalls (TA cheat sheet)

| Situation | Response |
|---|---|
| "My cell just shows nothing" | Did you `print()`? Only the last expression in a cell auto-displays. |
| `NameError: name 'x' is not defined` | The cell defining `x` hasn't been run (or runtime restarted). Run cells top-to-bottom. |
| `SyntaxError` pointing at a weird spot | Check the **line above** — often a missing `:` or unclosed quote/parenthesis. |
| `IndentationError` | Blocks under `if`/`for` need consistent 4-space indentation. |
| `=` vs `==` confusion | `=` assigns, `==` compares. `if x = 5:` is a syntax error. |
| Colab disconnected | Code is saved; memory isn't. Runtime → Run all. |
| "Do I need to install Python?" | Not for this course — Colab runs in the browser. (Point advanced students to Anaconda if they insist.) |
| Student without a Google account | Pair them up today; help them set up after class. |

## Timing Flex

- **Running short on time:** compress `while` loops and dict examples — they recur next lesson.
- **Running long / fast group:** add list slicing, `append()`, or nested loops; or have them plot two cities on one figure.
