#!/usr/bin/env python3
"""Build the WEEKLY guide (../weekly/CPSC444_Weekly_Guide.html) - the on-the-go pages
released week by week. Reuses generate_html_with_plots.py (same style, same figures)
but only for the modules listed in MODULES below.

To add a week:  1) write source/Module_XX_WeekN_<topic>.md   2) add a tuple to MODULES
               3) (optional) add figures: a figure_scripts/ script -> plots_data.json,
                  then a PLOT_MARKERS entry keyed by the heading the figure goes under
               4) run:  python generate_week2_html.py   (from the source/ folder)"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, 'generate_html_with_plots.py')
OUT = os.path.join(os.path.dirname(HERE), 'weekly', 'CPSC444_Weekly_Guide.html')

src = open(GEN).read()

# Modules 01, 02 and the Week 2 continuation only
src = re.sub(r'MODULES = \[.*?\n\]', """MODULES = [
    ('module1', 'Module_01_Foundations.md',
     'Module 01: Week 1: Foundations<span class="nav-sub">W1 &middot; 24 - 28 Aug</span>'),
    ('module2', 'Module_02_Statistical_Foundations.md',
     'M.01 &middot; Week 2: Statistical Foundations<span class="nav-sub">W2 &middot; 31 Aug - 4 Sep</span>'),
    ('module2b', 'Module_02b_First_Maps.md',
     'M.02 &middot; Week 2 (cont.): First Maps - Vector &amp; Raster<span class="nav-sub">M02 &middot; W2 &middot; 31 Aug - 4 Sep &middot; continuation</span>'),
    ('module3w3', 'Module_03_Week3_Coordinate_Systems.md',
     'M.03 &middot; Week 3: Coordinate Systems &amp; Transformations<span class="nav-sub">M03 &middot; W3 &middot; 7 - 11 Sep</span>'),
]""", src, count=1, flags=re.S)

# Drop the In-Class Activity and Practice Exercises sections from the web page
# (they stay in the markdown for the notebook / TA versions)
src = src.replace(
    "        with open(filepath, 'r', encoding='utf-8') as f:\n            content = f.read()\n",
    "        with open(filepath, 'r', encoding='utf-8') as f:\n            content = f.read()\n"
    "        if mod_id == 'module2b':\n"
    "            content = re.sub(r'## In-Class Activity: Think-Pair-Share.*?(?=## Course Materials)', '', content, flags=re.S)\n"
    "            content = content.replace('- [ ] Complete Practice Exercises 1-4 above in your own Colab notebook',\n"
    "                                      '- [ ] Work through the Week 2 First Maps Colab notebook top to bottom')\n", 1)

# Page headings use week names, not module numbers (markdown sources stay unchanged)
src = src.replace(
    "        html_content = md_to_html(content)\n",
    "        html_content = md_to_html(content)\n"
    "        for old, new in {'<h1>Module 01: Foundations</h1>': '<h1>Week 1: Foundations</h1>',\n"
    "                         '<h1>Module 02: Statistical Foundations</h1>': '<h1>Week 2: Statistical Foundations</h1>',\n"
    "                         '<h1>Module 02 (continued): First Maps</h1>': '<h1>Week 2 (continued): First Maps</h1>',\n"
    "                         '<h1>Module 03: Coordinate Systems & Transformations</h1>': '<h1>Week 3: Coordinate Systems & Transformations</h1>'}.items():\n"
    "            html_content = html_content.replace(old, new, 1)\n", 1)

# Figures for the Week 2 continuation (keys added to plots_data.json)
src = src.replace("PLOT_MARKERS = {\n    'module1': {", """PLOT_MARKERS = {
    'module3w3': {
        '### 2. Two Kinds of CRS': '''
<div class="plot-container">
    <img src="{mod03w3_degree_length}" alt="Length of one degree of longitude vs latitude" class="module-plot">
    <p class="plot-caption"><strong>Figure 3.1:</strong> One degree of latitude is about 111 km everywhere, but one degree of longitude shrinks toward the poles - about 85 km in Urbana. That is why degrees cannot be used as a unit of distance or area.</p>
</div>
''',
        '### 5. Converting with .to_crs()': '''
<div class="plot-container">
    <img src="{mod03w3_degrees_vs_meters}" alt="Same field in degrees and in UTM meters" class="module-plot">
    <p class="plot-caption"><strong>Figure 3.2:</strong> The Week 2 field and sample sites in EPSG:4326 (degrees, left) and after <code>.to_crs("EPSG:32616")</code> (UTM meters, right). Nothing moved on the ground - only the numbers on the axes changed, and now distances and areas can be measured.</p>
</div>
''',
        '### 6. What Actually Changes When You Convert': '''
<div class="plot-container">
    <img src="{mod03w3_projections}" alt="The continental US in three coordinate systems" class="module-plot">
    <p class="plot-caption"><strong>Figure 3.3:</strong> The same 48 states in three CRS. Over a whole country the flattening recipe visibly changes the shape: EPSG:4326 squashes east-west, Web Mercator (EPSG:3857) stretches the north, and Albers (EPSG:5070) keeps areas correct at the cost of curved edges. Over a single field the differences are invisible, but the numbers still change.</p>
</div>
''',
    },
    'module2b': {
        '### 1. From a Table to a Map': '''
<div class="plot-container">
    <img src="{mod02b_table_to_map}" alt="Table to map" class="module-plot">
    <p class="plot-caption"><strong>Figure 2.4:</strong> The same eight soil-sample sites as a table (left) and as a map (right). Adding longitude and latitude columns is all it takes to turn Week 1-2 data into spatial data.</p>
</div>
''',
        '### 2. Raster vs Vector Data': '''
<div class="plot-container">
    <img src="{mod03_raster_vector}" alt="Raster vs Vector" class="module-plot">
    <p class="plot-caption"><strong>Figure 2.5:</strong> Raster vs Vector data. Raster = grid of cells (like a photo). Vector = points, lines, polygons (like a drawing).</p>
</div>
''',
        '### 7. Raster Data: Create, Plot, Save, Read Back': '''
<div class="plot-container">
    <img src="{mod02b_overlay}" alt="Raster and vector overlay" class="module-plot">
    <p class="plot-caption"><strong>Figure 2.6:</strong> Three layers on one map: the simulated elevation raster underneath, the field boundary polygon (white), and the sample points colored by yield. This works only because all three layers share the same CRS.</p>
</div>
''',
        '### 8. Connecting Maps to Regression': '''
<div class="plot-container">
    <img src="{mod02b_regression_residuals}" alt="Regression and residual map" class="module-plot">
    <p class="plot-caption"><strong>Figure 2.7:</strong> Left: yield vs elevation at the 8 sites - the Week 2 view (weak fit, R² about 0.28). Right: the same regression's residuals drawn on the map. Blue (under-predicted) sites cluster in the north-center and red (over-predicted) sites sit at the edges - nearby sites share errors, which violates the independence assumption of Module 02.</p>
</div>
''',
    },
    'module1': {""", 1)

# Lines that start with inline markup (**bold**, `code`, [link]) must still be
# wrapped in <p>; only real block-level HTML (details, div, img...) is passed raw.
src = src.replace(
    "if content.strip() and not content.startswith('<'):",
    "if content.strip() and not re.match(r'\\s*<(/?details|summary|/?div|img|p|h\\d|/?ul|/?ol|li|/?table|tr|hr)\\b', content):")

# Style for the week/date subtitle lines in the sidebar
src = src.replace(".nav-link:hover {{",
                  ".nav-link .nav-sub {{ display: block; font-size: 0.8em; opacity: 0.85; margin-top: 3px; font-weight: 400; pointer-events: none; }}\n        .nav-link:hover {{")

# First module is the active section/nav item instead of 'home'
src = src.replace("mod_id == 'home'", "mod_id == MODULES[0][0]")

# Page title and sidebar header
src = src.replace('<title>CPSC 444 Complete Study Guide with Graphics</title>',
                  '<title>CPSC 444 Study Guide - Fall 2026</title>')
src = src.replace('<p>With Graphics</p>',
                  '<p>Spatial Statistics, Geospatial Analysis &amp; Agricultural Data Science</p>\n                <p>Fall 2026</p>')

# Output file
src = src.replace("output_file = os.path.join(BASE_PATH, 'CPSC444_Study_Guide_with_Graphics.html')",
                  f"output_file = {OUT!r}")
src = src.replace('print(f"📁 File: CPSC444_Study_Guide_with_Graphics.html")',
                  'print(f"📁 File: " + output_file)')

exec(compile(src, GEN, 'exec'), {'__file__': GEN, '__name__': '__main__'})
