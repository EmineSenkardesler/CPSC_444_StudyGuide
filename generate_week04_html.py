#!/usr/bin/env python3
"""Build the standalone Week 4 (Spatial Joins) HTML from the main generator.

Reads Week4_Spatial_Joins.md and week04_plots.json (figures made from the real
DIFM trial data with make_week04_plots logic) and writes the Week 4 page.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, 'generate_html_with_plots.py')
OUT = os.path.join(os.path.dirname(HERE), 'CPSC444_Week04_SpatialOperations.html')

src = open(GEN).read()

# Use this week's figures instead of the full guide's
src = src.replace("'plots_data.json'", "'week04_plots.json'")

# Single Week 4 entry in the sidebar
src = re.sub(r'MODULES = \[.*?\n\]', """MODULES = [
    ('week4', 'Week4_Spatial_Joins.md',
     'Week 4: Spatial Operations<span class="nav-sub">Joins &amp; overlays &middot; 14 - 18 Sep</span>'),
]""", src, count=1, flags=re.S)

# This week's figures, each under the step where it belongs
src = re.sub(r'PLOT_MARKERS = \{.*?\n\}', '''PLOT_MARKERS = {
    'week4': {
        '#### The data at a glance': """
<div class="plot-container">
    <img src="{w4_data}" alt="The two data layers" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.1:</strong> The two layers, plotted straight from the files. Left: 4,283 trial plots colored by nitrogen rate. Right: 177,495 yield monitor points colored by dry yield.</p>
</div>
""",
        '#### Merging operations on the map': """
<div class="plot-container">
    <img src="{w4_uniondis}" alt="Union and dissolve" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.2:</strong> Left: union_all() merges all 4,283 plots into one field outline. Right: dissolve(by="NitrogenRate") merges them into 6 shapes - one per treatment.</p>
</div>
""",
        '#### Cutting operations on the map': """
<div class="plot-container">
    <img src="{w4_cuts}" alt="Buffer, clip and difference" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.3:</strong> Left: buffer(120) makes the circle, clip() keeps only the 11,263 yield points inside it. Right: difference() cuts the circle out of the field.</p>
</div>
""",
        '#### Step 1 - Look before you join': """
<div class="plot-container">
    <img src="{w4_overlay}" alt="Trial plots and yield points overlaid" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.4:</strong> A few plots in the middle of the field. Left: the two layers just overlaid - purple trial plots, blue yield monitor points. Right: after the spatial join, each point is colored by the plot it fell in.</p>
</div>
""",
        '#### Step 3 - Aggregate: one number per plot': """
<div class="plot-container">
    <img src="{w4_plotmap}" alt="Plots colored by mean yield" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.5:</strong> The result of join + aggregate: each trial plot colored by the mean dry yield of the 177,457 points that fell inside it.</p>
</div>
""",
        '#### Step 4 - The payoff': """
<div class="plot-container">
    <img src="{w4_response}" alt="Yield by nitrogen rate" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.6:</strong> What the join unlocks: treatment (nitrogen rate, from the polygons) against response (plot mean yield, from the points).</p>
</div>
""",
    },
}''', src, count=1, flags=re.S)

# Let markers target #### (h4) step headings too
src = src.replace("if marker.startswith('### '):",
                  "if marker.startswith('#### '):\n"
                  "                    tag, text = 'h4', marker[5:]\n"
                  "                elif marker.startswith('### '):")

# Convert markdown pipe tables to HTML before the line-based converter runs
src = src.replace("def md_to_html(text):", '''def tables_to_html(text):
    """Turn markdown pipe tables into one-line HTML tables (passed through untouched)."""
    out, table = [], []
    def flush():
        if not table:
            return
        rows = [[c.strip() for c in r.strip().strip('|').split('|')] for r in table]
        rows = [r for r in rows if not all(set(c) <= set('-: ') for c in r)]
        html = '<table class="md-table"><tr>' + ''.join(f'<th>{c}</th>' for c in rows[0]) + '</tr>'
        for r in rows[1:]:
            html += '<tr>' + ''.join('<td>' + re.sub(r'`([^`]+)`', r'<code>\\1</code>', c) + '</td>' for c in r) + '</tr>'
        out.append(html + '</table>')
        table.clear()
    for line in text.split('\\n'):
        if line.strip().startswith('|') and line.strip().endswith('|'):
            table.append(line)
        else:
            flush(); out.append(line)
    flush()
    return '\\n'.join(out)

def md_to_html(text):''')
src = src.replace("html_content = md_to_html(content)",
                  "html_content = md_to_html(tables_to_html(content))")
src = src.replace("a {{ color: #667eea; }}",
                  "a {{ color: #667eea; }}\\n"
                  "        .md-table {{ border-collapse: collapse; margin: 20px 0; width: 100%; }}\\n"
                  "        .md-table th, .md-table td {{ border: 1px solid #ddd; padding: 10px 14px; text-align: left; }}\\n"
                  "        .md-table th {{ background: #667eea; color: white; }}\\n"
                  "        .md-table tr:nth-child(even) {{ background: #f7f7fb; }}")

# Style for the subtitle line in the sidebar
src = src.replace(".nav-link:hover {{",
                  ".nav-link .nav-sub {{ display: block; font-size: 0.8em; opacity: 0.85; margin-top: 3px; font-weight: 400; pointer-events: none; }}\n        .nav-link:hover {{")

# First entry is the active section/nav item instead of 'home'
src = src.replace("mod_id == 'home'", "mod_id == MODULES[0][0]")

# Page title and sidebar header
src = src.replace('<title>CPSC 444 Complete Study Guide with Graphics</title>',
                  '<title>CPSC 444 Week 4 - Spatial Operations</title>')
src = src.replace('<p>With Graphics</p>',
                  '<p>Spatial Statistics, Geospatial Analysis &amp; Agricultural Data Science</p>\n                <p>Fall 2026</p>')

# Output file
src = src.replace("output_file = os.path.join(BASE_PATH, 'CPSC444_Study_Guide_with_Graphics.html')",
                  f"output_file = {OUT!r}")
src = src.replace('print(f"📁 File: CPSC444_Study_Guide_with_Graphics.html")',
                  'print(f"📁 File: " + output_file)')

exec(compile(src, GEN, 'exec'), {'__file__': GEN, '__name__': '__main__'})
