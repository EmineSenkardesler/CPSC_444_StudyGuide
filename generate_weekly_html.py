#!/usr/bin/env python3
"""One-off: build a standalone Modules 01-02 HTML from the existing generator."""
import os, re

GEN = '/Users/emine2/Documents/CLASSES/03_2025-FALL/TA-2025-FALL/cpsc444-study-guide/generate_html_with_plots.py'
OUT = '/Users/emine2/Documents/CLASSES/03_2025-FALL/TA-2025-FALL/CPSC444_Module01_Foundations.html'

src = open(GEN).read()

# Only Modules 01 and 02
src = re.sub(r'MODULES = \[.*?\n\]', """MODULES = [
    ('module1', 'Module_01_Foundations.md',
     'Module 01: Foundations<span class="nav-sub">W1 &middot; 24 - 28 Aug</span>'),
    ('module2', 'Module_02_Statistical_Foundations.md',
     'M.01 &middot; Week 2: Statistical Foundations<span class="nav-sub">31 Aug - 4 Sep</span>'),
]""", src, count=1, flags=re.S)

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
