#!/usr/bin/env python3
"""Generate HTML with embedded plot images"""

import json
import re
import os
from urllib.parse import quote

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Rewrite local /tmp/cpsc444-study/ notebook links to the course GitHub repo
GITHUB_BASE = 'https://github.com/acesillinois/cpsc444-F2025/blob/main/'
# Filenames that differ between the guide text and the actual repo
GITHUB_PATH_FIXES = {
    'python_notebooks/ToyRaster_Contiguity_Extended_pub.ipynb':
        'python_notebooks/ToyRaster_Contiguity_Extended _pub.ipynb',
    'w01-exercises/Geospatial_Overlay_Tutorial.ipynb':
        'w01-exercises/Geospatial_Overlay_Tutorial_20250915_201234.ipynb',
    'w01-exercises/TrialDesign_SpatialMapping_Tutorial.ipynb':
        'w01-exercises/TrialDesign_SpatialMapping_Tutorial_CPSC444_09_17_2025.ipynb',
}

def rewrite_github_links(html_text):
    """Point href="/tmp/cpsc444-study/..." links at the GitHub repo instead."""
    def repl(m):
        path = GITHUB_PATH_FIXES.get(m.group(1), m.group(1))
        return f'href="{GITHUB_BASE}{quote(path)}" target="_blank" rel="noopener"'
    return re.sub(r'href="/tmp/cpsc444-study/([^"]+)"', repl, html_text)

# Load plots
print("Loading plots data...")
with open(os.path.join(BASE_PATH, 'plots_data.json'), 'r') as f:
    PLOTS = json.load(f)
print(f"✓ Loaded {len(PLOTS)} plots ({sum(len(v) for v in PLOTS.values())/1024:.1f} KB total)")

MODULES = [
    ('home', 'README.md', 'Home & Overview'),
    ('paths', 'Study_Paths.md', 'Study Paths'),
    ('module1', 'Module_01_Foundations.md', 'Module 01: Foundations'),
    ('module2', 'Module_02_Statistical_Foundations.md', 'Module 02: Statistical Foundations'),
    ('module3', 'Module_03_Geospatial_Fundamentals.md', 'Module 03: Geospatial Fundamentals'),
    ('module4', 'Module_04_Spatial_Statistics.md', 'Module 04: Spatial Statistics'),
    ('module5', 'Module_05_Advanced_Regression.md', 'Module 05: Advanced Regression'),
    ('module6', 'Module_06_Mixed_Models.md', 'Module 06: Mixed Models'),
    ('module7', 'Module_07_Machine_Learning.md', 'Module 07: Machine Learning'),
    ('module8', 'Module_08_Specialized_Applications.md', 'Module 08: Specialized Applications'),
    ('reference', 'Quick_Reference.md', 'Quick Reference'),
]

# Define plot insertion points with markers.
# Markers may be '## ' (h2) or '### ' (h3) headings; each plot is inserted
# right after the section where its concept is explained.
PLOT_MARKERS = {
    'module1': {
        '### 7. Simple Linear Regression': '''
<div class="plot-container">
    <img src="{mod01_regression}" alt="Simple Linear Regression" class="module-plot">
    <p class="plot-caption"><strong>Figure 1.1:</strong> Simple linear regression showing relationship between rainfall and crop yield. The line of best fit minimizes prediction errors.</p>
</div>
''',
        '### 6. Probability Distributions': '''
<div class="plot-container">
    <img src="{mod01_distributions}" alt="Common Distributions" class="module-plot">
    <p class="plot-caption"><strong>Figure 1.2:</strong> Common probability distributions: Normal (bell curve), Binomial (discrete outcomes), Poisson (count data), and Exponential (time between events).</p>
</div>
''',
        '### 8. Q-Q Plots (Quantile-Quantile Plots)': '''
<div class="plot-container">
    <img src="{mod01_qqplot}" alt="Q-Q Plots" class="module-plot">
    <p class="plot-caption"><strong>Figure 1.3:</strong> Q-Q plots for assessing normality. Left: normal data falls on diagonal line. Right: skewed data curves away from line.</p>
</div>
'''
    },
    'module2': {
        '### 3. Logistic Regression': '''
<div class="plot-container">
    <img src="{mod02_sigmoid}" alt="Sigmoid Function" class="module-plot">
    <p class="plot-caption"><strong>Figure 2.1:</strong> Logistic regression sigmoid function. Converts any input to probability between 0 and 1. The decision boundary is at P=0.5.</p>
</div>
''',
        '### 5. Model Evaluation Metrics': '''
<div class="plot-container">
    <img src="{mod02_confusion_matrix}" alt="Confusion Matrix" class="module-plot">
    <p class="plot-caption"><strong>Figure 2.2:</strong> Confusion matrix example showing model performance. True Negatives (TN) and True Positives (TP) are correct predictions. False Positives (FP) and False Negatives (FN) are errors.</p>
</div>

<div class="plot-container">
    <img src="{mod02_roc_curve}" alt="ROC Curve" class="module-plot">
    <p class="plot-caption"><strong>Figure 2.3:</strong> ROC (Receiver Operating Characteristic) curve. Area Under Curve (AUC) near 1.0 indicates excellent model performance. Random classifier would follow the diagonal dashed line.</p>
</div>
'''
    },
    'module3': {
        '### 2. Raster vs Vector Data': '''
<div class="plot-container">
    <img src="{mod03_raster_vector}" alt="Raster vs Vector" class="module-plot">
    <p class="plot-caption"><strong>Figure 3.1:</strong> Raster vs Vector data. Raster = grid of cells (like photos). Vector = points, lines, polygons (like drawings).</p>
</div>
''',
        '### 5. Kriging Interpolation': '''
<div class="plot-container">
    <img src="{mod03_kriging_example}" alt="Kriging Process" class="module-plot">
    <p class="plot-caption"><strong>Figure 3.2:</strong> Kriging interpolation process. Step 1: Sample points with known values. Step 2: Use spatial correlation to weight nearby points. Step 3: Generate continuous predicted surface.</p>
</div>

<div class="plot-container">
    <img src="{mod03_semivariogram}" alt="Semivariogram" class="module-plot">
    <p class="plot-caption"><strong>Figure 3.3:</strong> Semivariogram components. Nugget = variance at distance zero. Sill = maximum variance. Range = distance where points become uncorrelated.</p>
</div>
'''
    },
    'module4': {
        '### 3. Variogram Models - Choosing the Right One': '''
<div class="plot-container">
    <img src="{mod04_variogram_models}" alt="Variogram Models" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.1:</strong> Comparison of variogram models. Spherical (most common, levels off at range), Exponential (gradual approach to sill), Gaussian (very smooth, for continuous processes).</p>
</div>
''',
        '### 4. Rook vs Queen Contiguity': '''
<div class="plot-container">
    <img src="{mod04_contiguity}" alt="Contiguity" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.2:</strong> Rook vs Queen contiguity. Rook = 4 neighbors (share edge, like rook in chess). Queen = 8 neighbors (share edge or corner, like queen in chess).</p>
</div>
''',
        '### 5. Spatial Correlograms': '''
<div class="plot-container">
    <img src="{mod04_correlogram}" alt="Correlogram" class="module-plot">
    <p class="plot-caption"><strong>Figure 4.3:</strong> Spatial correlogram showing exponential decay of correlation with distance. High correlation at small distances, decreasing to zero at larger distances.</p>
</div>
'''
    },
    'module5': {
        '### 3. Lasso Regression (L1 Regularization)': '''
<div class="plot-container">
    <img src="{mod05_ridge_lasso}" alt="Ridge vs Lasso" class="module-plot">
    <p class="plot-caption"><strong>Figure 5.1:</strong> Ridge vs Lasso regularization. Ridge (L2) shrinks all coefficients but keeps them all. Lasso (L1) can eliminate coefficients entirely (sets to zero), providing feature selection.</p>
</div>
''',
        '### 4. Geographically Weighted Regression (GWR)': '''
<div class="plot-container">
    <img src="{mod05_gwr_concept}" alt="GWR Concept" class="module-plot">
    <p class="plot-caption"><strong>Figure 5.2:</strong> Geographically Weighted Regression (GWR) concept. Regular regression assumes same relationship everywhere. GWR allows relationships to vary across space - different coefficients for different locations.</p>
</div>
'''
    },
    'module6': {
        '### 4. Random Slope Model': '''
<div class="plot-container">
    <img src="{mod06_random_effects}" alt="Random Effects" class="module-plot">
    <p class="plot-caption"><strong>Figure 6.1:</strong> Random intercept vs random slope models. Random intercept: parallel lines (different baselines, same response). Random slope: non-parallel lines (different baselines AND different responses).</p>
</div>
'''
    },
    'module7': {
        '### 2. Random Forest': '''
<div class="plot-container">
    <img src="{mod07_decision_boundaries}" alt="Decision Boundaries" class="module-plot">
    <p class="plot-caption"><strong>Figure 7.1:</strong> Linear vs non-linear decision boundaries. Logistic regression creates linear boundary. Random Forest and Neural Networks can create complex non-linear boundaries to better separate classes.</p>
</div>

<div class="plot-container">
    <img src="{mod07_feature_importance}" alt="Feature Importance" class="module-plot">
    <p class="plot-caption"><strong>Figure 7.2:</strong> Feature importance from Random Forest. Shows which variables contribute most to predictions. Rainfall and temperature are most important for yield prediction in this example.</p>
</div>
'''
    },
}

def md_to_html(text):
    """Simple markdown to HTML converter"""
    lines = text.split('\n')
    html = []
    in_code = False
    in_list = False

    for line in lines:
        if line.strip().startswith('```'):
            if not in_code:
                html.append('<pre><code>')
                in_code = True
            else:
                html.append('</code></pre>')
                in_code = False
            continue

        if in_code:
            html.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            continue

        # Headers
        if line.startswith('#### '):
            html.append(f'<h4>{line[5:]}</h4>')
        elif line.startswith('### '):
            html.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            html.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            html.append(f'<h1>{line[2:]}</h1>')
        elif line.strip() == '---':
            html.append('<hr>')
        elif line.strip().startswith('- [ ]'):
            if not in_list:
                html.append('<ul class="checkbox-list">')
                in_list = True
            content = line.strip()[5:]
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            html.append(f'<li>{content}</li>')
        elif line.strip().startswith('- '):
            if not in_list:
                html.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            html.append(f'<li>{content}</li>')
        elif not line.strip():
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append('')
        else:
            if in_list:
                html.append('</ul>')
                in_list = False
            content = line
            content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            if content.strip() and not content.startswith('<'):
                html.append(f'<p>{content}</p>')
            elif content.strip():
                html.append(content)

    if in_list:
        html.append('</ul>')

    return '\n'.join(html)

def generate_html():
    """Generate complete HTML with embedded plots"""

    sections_html = []

    for idx, (mod_id, filename, title) in enumerate(MODULES):
        # Read module content
        filepath = os.path.join(BASE_PATH, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Convert to HTML
        html_content = md_to_html(content)
        html_content = rewrite_github_links(html_content)

        # Insert plots for this module
        if mod_id in PLOT_MARKERS:
            for marker, plot_html in PLOT_MARKERS[mod_id].items():
                # Format plot HTML with actual base64 data
                formatted_plots = plot_html.format(**PLOTS)
                # Insert after the marker heading (h2 for '## ', h3 for '### ')
                if marker.startswith('### '):
                    tag, text = 'h3', marker[4:]
                else:
                    tag, text = 'h2', marker[3:]
                heading = f'<{tag}>{text}</{tag}>'
                if heading not in html_content:
                    print(f"⚠️  Marker not found in {mod_id}: {marker}")
                html_content = html_content.replace(heading, f'{heading}{formatted_plots}', 1)

        # Navigation buttons
        prev_btn = '<button class="btn btn-secondary" disabled>← Previous</button>'
        next_btn = '<button class="btn btn-primary">Next →</button>'

        if idx > 0:
            prev_id = MODULES[idx-1][0]
            prev_btn = f'<button class="btn btn-secondary" onclick="showSection(\'{prev_id}\')">← Previous</button>'
        if idx < len(MODULES) - 1:
            next_id = MODULES[idx+1][0]
            next_btn = f'<button class="btn btn-primary" onclick="showSection(\'{next_id}\')">Next →</button>'

        section_html = f'''
        <section id="{mod_id}" class="content-section{' active' if mod_id == 'home' else ''}">
            {html_content}
            <div class="nav-buttons">
                {prev_btn}
                {next_btn}
            </div>
        </section>'''

        sections_html.append(section_html)

    # Generate navigation
    nav_items = []
    for mod_id, filename, title in MODULES:
        nav_items.append(f'''
                <li class="nav-item">
                    <a class="nav-link{' active' if mod_id == 'home' else ''}" onclick="showSection('{mod_id}')">
                        {title}
                    </a>
                </li>''')

    # Complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPSC 444 Complete Study Guide with Graphics</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        .container {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 280px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; overflow-y: auto; }}
        .sidebar-header {{ padding: 20px; background: rgba(0,0,0,0.2); }}
        .sidebar-header h1 {{ font-size: 1.4em; }}
        .nav-menu {{ list-style: none; padding: 10px 0; }}
        .nav-item {{ margin: 2px 10px; }}
        .nav-link {{ display: block; padding: 12px 15px; color: white; border-radius: 8px; cursor: pointer; transition: 0.3s; }}
        .nav-link:hover {{ background: rgba(255,255,255,0.15); transform: translateX(5px); }}
        .nav-link.active {{ background: rgba(255,255,255,0.25); font-weight: 600; }}
        .main-content {{ flex: 1; overflow-y: auto; background: white; }}
        .content-section {{ display: none; padding: 40px 60px; max-width: 1000px; margin: 0 auto; }}
        .content-section.active {{ display: block; }}
        h1 {{ color: #667eea; font-size: 2.5em; margin-bottom: 10px; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        h2 {{ color: #764ba2; font-size: 2em; margin-top: 30px; margin-bottom: 15px; }}
        h3 {{ color: #555; font-size: 1.5em; margin-top: 25px; margin-bottom: 12px; }}
        h4 {{ color: #666; font-size: 1.2em; margin-top: 20px; }}
        p {{ margin-bottom: 15px; }}
        ul, ol {{ margin: 15px 0 15px 30px; }}
        pre {{ background: #2d2d2d; color: #f8f8f2; padding: 20px; border-radius: 8px; margin: 20px 0; overflow-x: auto; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; color: #d63384; }}
        pre code {{ background: transparent; color: #f8f8f2; }}
        .checkbox-list {{ list-style: none; margin-left: 0; }}
        .checkbox-list li:before {{ content: "☐ "; color: #667eea; font-weight: bold; margin-right: 8px; }}
        .nav-buttons {{ display: flex; justify-content: space-between; margin-top: 40px; padding-top: 20px; border-top: 2px solid #eee; }}
        .btn {{ padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 1em; }}
        .btn-primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
        .btn-secondary {{ background: #6c757d; color: white; }}
        .plot-container {{ margin: 30px 0; text-align: center; background: #f9f9f9; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; }}
        .module-plot {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .plot-caption {{ margin-top: 15px; font-style: italic; color: #555; }}
        a {{ color: #667eea; }}
        strong {{ color: #764ba2; }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <div class="sidebar-header">
                <h1>CPSC 444</h1>
                <p>With Graphics</p>
            </div>
            <ul class="nav-menu">
{''.join(nav_items)}
            </ul>
        </nav>
        <main class="main-content">
{''.join(sections_html)}
        </main>
    </div>
    <script>
        function showSection(id) {{
            document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelector('.main-content').scrollTop = 0;
        }}
        console.log('Study Guide with {len(PLOTS)} plots loaded!');
    </script>
</body>
</html>'''

    return html

# Generate and save
print("\nGenerating HTML...")
html_output = generate_html()

output_file = os.path.join(BASE_PATH, 'CPSC444_Study_Guide_with_Graphics.html')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_output)

file_size = len(html_output)
print(f"\n✅ Success!")
print(f"📁 File: CPSC444_Study_Guide_with_Graphics.html")
print(f"📊 Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
print(f"🖼️  Plots: {len(PLOTS)} graphics embedded")
print(f"\n🌐 Open in browser to view!")
