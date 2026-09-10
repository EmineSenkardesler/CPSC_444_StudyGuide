#!/usr/bin/env python3
"""Build the FULL 8-module reference guide -> ../full_guide/CPSC444_Study_Guide_with_Graphics.html
Thin wrapper: runs generate_html_with_plots.py unchanged, only redirecting the output path.
Run from the source/ folder:  python build_full_guide.py"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, 'generate_html_with_plots.py')
OUT = os.path.join(os.path.dirname(HERE), 'full_guide', 'CPSC444_Study_Guide_with_Graphics.html')
src = open(GEN).read()
src = src.replace("output_file = os.path.join(BASE_PATH, 'CPSC444_Study_Guide_with_Graphics.html')", f"output_file = {OUT!r}")
src = src.replace('print(f"📁 File: CPSC444_Study_Guide_with_Graphics.html")', 'print(f"📁 File: " + output_file)')
exec(compile(src, GEN, 'exec'), {'__file__': GEN, '__name__': '__main__'})

# Fixed-name copy for GitHub Pages: .../CPSC_444_StudyGuide/full_guide.html
import shutil
DOCS = os.path.join(os.path.dirname(HERE), 'docs')
os.makedirs(DOCS, exist_ok=True)
shutil.copyfile(OUT, os.path.join(DOCS, 'full_guide.html'))
print("🌐 Pages copy: docs/full_guide.html")
