#!/usr/bin/env python3
"""Build the student site.

Outputs (all self-contained HTML, figures embedded):
  ../docs/index.html          landing page: the weeks published so far
  ../docs/week1.html, week2.html, week2_maps.html, week3.html ...   one page per week
  ../docs/all_weeks.html      every week on one page (sidebar switches sections)
  ../weekly/CPSC444_WeeklyGuide_W<latest>_<date>.html   dated copy of all_weeks.html

docs/ is served by GitHub Pages from the weekly-guide branch, so:  build + push = published.

TO ADD A WEEK: write source/WeekN_<topic>.md, append one dict to WEEKS below, run this script.
TO ADD A FIGURE: a figure_scripts/ script saves a base64 PNG into plots_data.json under a new key;
                 add an entry to EXTRA_MARKERS keyed by the exact heading the figure goes under.
Run from the source/ folder:  python build_site.py
"""
import os, re, glob, datetime, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, 'docs')
WEEKLY = os.path.join(ROOT, 'weekly')
GEN = os.path.join(HERE, 'generate_html_with_plots.py')

SITE_TITLE = 'CPSC 444 Weekly Guide - Fall 2026'
SUBTITLE = 'Spatial Statistics, Geospatial Analysis &amp; Agricultural Data Science'
SEMESTER = 'Fall 2026'

# ---------------------------------------------------------------- the weeks
# slug      -> file name in docs/ (slug.html) - never change a slug once shared
# md        -> markdown source in source/
# title     -> page heading + sidebar label     dates -> sidebar subtitle
# blurb     -> one line on the landing page
# base_key  -> key of the original generator's PLOT_MARKERS to reuse its figures (or None)
# h1_from   -> the markdown's own H1, replaced by `title` (so shared module files stay untouched)
# cut       -> (start heading, end heading) blocks to drop from the web version
WEEKS = [
    dict(slug='week1', md='Module_01_Foundations.md', base_key='module1',
         title='Week 1: Foundations', dates='24 - 28 Aug',
         h1_from='Module 01: Foundations',
         blurb='Python basics, plotting, summary statistics, distributions, simple regression.'),
    dict(slug='week2', md='Module_02_Statistical_Foundations.md', base_key='module2',
         title='Week 2: Statistical Foundations', dates='31 Aug - 4 Sep',
         h1_from='Module 02: Statistical Foundations',
         blurb='Multiple and logistic regression, model evaluation, the five regression assumptions.'),
    dict(slug='week2_maps', md='Module_02b_First_Maps.md', base_key=None,
         title='Week 2 (continued): First Maps', dates='31 Aug - 4 Sep',
         h1_from='Module 02 (continued): First Maps',
         cut=[('## In-Class Activity: Think-Pair-Share', '## Course Materials')],
         replace=[('- [ ] Complete Practice Exercises 1-4 above in your own Colab notebook',
                   '- [ ] Work through the Week 2 First Maps Colab notebook top to bottom')],
         blurb='Vector vs raster, GeoDataFrames, polygons, first contact with CRS, GeoTIFFs, raster values at points, mapping regression residuals.'),
    dict(slug='week3', md='Week3_Coordinate_Systems.md', base_key=None,
         title='Week 3: Coordinate Systems &amp; Transformations', dates='7 - 11 Sep',
         h1_from='Week 3: Coordinate Systems & Transformations',
         blurb='Geographic vs projected CRS, EPSG codes, .to_crs() vs .set_crs(), what changes when you convert, reprojecting rasters.'),
]

# Figures for the weekly-only pages (keys live in plots_data.json)
def _fig(key, caption, alt):
    return f'''
<div class="plot-container">
    <img src="{{{key}}}" alt="{alt}" class="module-plot">
    <p class="plot-caption">{caption}</p>
</div>
'''
EXTRA_MARKERS = {
    'week2_maps': {
        '### 1. From a Table to a Map': _fig('mod02b_table_to_map', '<strong>Figure 2.4:</strong> The same eight soil-sample sites as a table (left) and as a map (right). Adding longitude and latitude columns is all it takes to turn Week 1-2 data into spatial data.', 'Table to map'),
        '### 2. Raster vs Vector Data': _fig('mod03_raster_vector', '<strong>Figure 2.5:</strong> Raster vs Vector data. Raster = grid of cells (like a photo). Vector = points, lines, polygons (like a drawing).', 'Raster vs Vector'),
        '### 7. Raster Data: Create, Plot, Save, Read Back': _fig('mod02b_overlay', '<strong>Figure 2.6:</strong> Three layers on one map: the simulated elevation raster underneath, the field boundary polygon (white), and the sample points colored by yield. This works only because all three layers share the same CRS.', 'Raster and vector overlay'),
        '### 8. Connecting Maps to Regression': _fig('mod02b_regression_residuals', '<strong>Figure 2.7:</strong> Left: yield vs elevation at the 8 sites - the Week 2 view (weak fit, R² about 0.28). Right: the same regression\'s residuals drawn on the map. Blue (under-predicted) sites cluster in the north-center and red (over-predicted) sites sit at the edges - nearby sites share errors, which violates the independence assumption of Week 2.', 'Regression and residual map'),
    },
    'week3': {
        '### 2. Two Kinds of CRS': _fig('mod03w3_degree_length', '<strong>Figure 3.1:</strong> One degree of latitude is about 111 km everywhere, but one degree of longitude shrinks toward the poles - about 85 km in Urbana. That is why degrees cannot be used as a unit of distance or area.', 'Length of one degree of longitude vs latitude'),
        '### 5. Converting with .to_crs()': _fig('mod03w3_degrees_vs_meters', '<strong>Figure 3.2:</strong> The Week 2 field and sample sites in EPSG:4326 (degrees, left) and after <code>.to_crs("EPSG:32616")</code> (UTM meters, right). Nothing moved on the ground - only the numbers on the axes changed, and now distances and areas can be measured.', 'Same field in degrees and in UTM meters'),
        '### 6. What Actually Changes When You Convert': _fig('mod03w3_projections', '<strong>Figure 3.3:</strong> The same 48 states in three CRS. Over a whole country the flattening recipe visibly changes the shape: EPSG:4326 squashes east-west, Web Mercator (EPSG:3857) stretches the north, and Albers (EPSG:5070) keeps areas correct at the cost of curved edges. Over a single field the differences are invisible, but the numbers still change.', 'The continental US in three coordinate systems'),
    },
}

# ------------------------------------------- load the shared converter + style
gen_src = open(GEN, encoding='utf-8').read()
gen_src = gen_src.split('# Generate and save')[0]          # keep functions/constants, skip the full-guide build
# lines that START with inline markup (**bold**, `code`) must still be wrapped in <p>
gen_src = gen_src.replace(
    "if content.strip() and not content.startswith('<'):",
    "if content.strip() and not re.match(r'\\s*<(/?details|summary|/?div|img|p|h\\d|/?ul|/?ol|li|/?table|tr|hr)\\b', content):")
ns = {'__file__': GEN, '__name__': 'shared_generator'}
exec(compile(gen_src, GEN, 'exec'), ns)
md_to_html, rewrite_github_links, PLOTS, BASE_MARKERS = ns['md_to_html'], ns['rewrite_github_links'], ns['PLOTS'], ns['PLOT_MARKERS']
CSS = re.search(r'<style>(.*?)</style>', gen_src, re.S).group(1).replace('{{', '{').replace('}}', '}')
CSS += '''
        .nav-link .nav-sub { display: block; font-size: 0.8em; opacity: 0.85; margin-top: 3px; font-weight: 400; pointer-events: none; }
        .nav-link { text-decoration: none; }
        .nav-sep { margin: 14px 24px 6px; font-size: 0.75em; letter-spacing: .08em; text-transform: uppercase; opacity: .7; }
        .btn-link { text-decoration: none; display: inline-block; }
        .week-card { border: 2px solid #e0e0e0; border-radius: 10px; padding: 18px 22px; margin: 16px 0; background: #fafafa; }
        .week-card h3 { margin: 0 0 4px; }
        .week-card h3 a { text-decoration: none; }
        .week-card .dates { color: #777; font-size: .9em; }
        .week-card p { margin: 8px 0 0; }
        .week-card.full { border-color: #764ba2; background: #f6f2fb; }
'''

# ------------------------------------------------------------ page pieces
def week_body(w):
    text = open(os.path.join(HERE, w['md']), encoding='utf-8').read()
    for start, end in w.get('cut', []):
        text = re.sub(re.escape(start) + r'.*?(?=' + re.escape(end) + ')', '', text, flags=re.S)
    for a, b in w.get('replace', []):
        text = text.replace(a, b)
    body = rewrite_github_links(md_to_html(text))
    body = body.replace(f"<h1>{w['h1_from']}</h1>", f"<h1>{w['title']}</h1>", 1)
    markers = dict(BASE_MARKERS.get(w['base_key'], {}) if w['base_key'] else {})
    markers.update(EXTRA_MARKERS.get(w['slug'], {}))
    for marker, plot_html in markers.items():
        tag, txt = ('h3', marker[4:]) if marker.startswith('### ') else ('h2', marker[3:])
        heading = f'<{tag}>{txt}</{tag}>'
        if heading not in body:
            print(f"  warning: figure marker not found in {w['slug']}: {marker}")
        body = body.replace(heading, heading + plot_html.format(**PLOTS), 1)
    return body

def sidebar(active, mode):
    """mode='links': week entries are hrefs to separate files; mode='sections': onclick switching.
    Every page: the published weeks. Nothing else."""
    items = ['<li class="nav-sep">Weeks</li>']
    for w in WEEKS:
        act = ' active' if w['slug'] == active else ''
        if mode == 'links':
            items.append(f'<li class="nav-item"><a class="nav-link{act}" href="{w["slug"]}.html">{w["title"]}<span class="nav-sub">{w["dates"]}</span></a></li>')
        else:
            items.append(f'<li class="nav-item"><a class="nav-link{act}" onclick="showSection(\'{w["slug"]}\')">{w["title"]}<span class="nav-sub">{w["dates"]}</span></a></li>')
    return '\n'.join(items)

def shell(title, nav_html, main_html, script=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{CSS}</style>
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <div class="sidebar-header">
                <h1>CPSC 444</h1>
                <p>{SUBTITLE}</p>
                <p>{SEMESTER}</p>
            </div>
            <ul class="nav-menu">
{nav_html}
            </ul>
        </nav>
        <main class="main-content">
{main_html}
        </main>
    </div>
    <script>{script}</script>
</body>
</html>'''

def nav_buttons(i):
    prev = f'<a class="btn btn-secondary btn-link" href="{WEEKS[i-1]["slug"]}.html">← {WEEKS[i-1]["title"]}</a>' if i > 0 else ''
    nxt = f'<a class="btn btn-primary btn-link" href="{WEEKS[i+1]["slug"]}.html">{WEEKS[i+1]["title"]} →</a>' if i < len(WEEKS) - 1 else ''
    return f'<div class="nav-buttons">{prev}{nxt}</div>'

def plain(s):  # strip html entities for <title>
    return s.replace('&amp;', '&')

# ------------------------------------------------------------------ build
os.makedirs(DOCS, exist_ok=True); os.makedirs(WEEKLY, exist_ok=True)
open(os.path.join(DOCS, '.nojekyll'), 'w').close()
bodies = {w['slug']: week_body(w) for w in WEEKS}

# one page per week
for i, w in enumerate(WEEKS):
    main = f'<section class="content-section active">\n{bodies[w["slug"]]}\n{nav_buttons(i)}\n</section>'
    open(os.path.join(DOCS, f'{w["slug"]}.html'), 'w', encoding='utf-8').write(
        shell(f'{plain(w["title"])} - CPSC 444', sidebar(w['slug'], 'links'), main))
    print(f"  docs/{w['slug']}.html")

# landing page
cards = ''.join(f'''
<div class="week-card">
    <h3><a href="{w['slug']}.html">{w['title']}</a></h3>
    <span class="dates">{w['dates']}</span>
    <p>{w['blurb']}</p>
</div>''' for w in WEEKS)
cards += '''
<div class="week-card">
    <h3><a href="all_weeks.html">All weeks on one page</a></h3>
    <span class="dates">same content as the weekly pages</span>
    <p>Every published week in a single page with a section switcher - handy for searching (Ctrl/Cmd+F) across weeks.</p>
</div>'''
landing = f'''<section class="content-section active">
<h1>CPSC 444 Weekly Guide</h1>
<p style="color:#764ba2;font-weight:600;font-size:1.1em">{SUBTITLE} &middot; {SEMESTER}</p>
<p>A new page is published each week to match what was covered in class. These are running notes, not the finished course text: they are short, example-driven and get edited as the semester goes. Bookmark this page - the links below never change.</p>
<p><em>Last updated: {datetime.date.today():%d %b %Y} &middot; {len(WEEKS)} pages published</em></p>
{cards}
</section>'''
open(os.path.join(DOCS, 'index.html'), 'w', encoding='utf-8').write(shell(SITE_TITLE, sidebar('index', 'links'), landing))
print("  docs/index.html")

# all weeks on one page (section switcher, like the original guide)
sections = []
for i, w in enumerate(WEEKS):
    prev = f'<button class="btn btn-secondary" onclick="showSection(\'{WEEKS[i-1]["slug"]}\')">← Previous</button>' if i > 0 else '<button class="btn btn-secondary" disabled>← Previous</button>'
    nxt = f'<button class="btn btn-primary" onclick="showSection(\'{WEEKS[i+1]["slug"]}\')">Next →</button>' if i < len(WEEKS) - 1 else '<button class="btn btn-primary" disabled>Next →</button>'
    sections.append(f'<section id="{w["slug"]}" class="content-section{" active" if i == 0 else ""}">\n{bodies[w["slug"]]}\n<div class="nav-buttons">{prev}{nxt}</div>\n</section>')
script = '''
        function showSection(id) {
            document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            if (event && event.target) event.target.classList.add('active');
            document.querySelector('.main-content').scrollTop = 0;
        }'''
all_weeks = shell(SITE_TITLE + ' (all weeks)', sidebar(WEEKS[0]['slug'], 'sections'), '\n'.join(sections), script)
open(os.path.join(DOCS, 'all_weeks.html'), 'w', encoding='utf-8').write(all_weeks)
print("  docs/all_weeks.html")

# dated copy of the all-weeks page in weekly/
latest = 'W' + re.search(r'Week (\d+)', WEEKS[-1]['title']).group(1)
out_name = f"CPSC444_WeeklyGuide_{latest}_{datetime.date.today():%Y-%m-%d}.html"
for old in glob.glob(os.path.join(WEEKLY, 'CPSC444_WeeklyGuide_*.html')):
    if os.path.basename(old) != out_name:
        os.remove(old)
open(os.path.join(WEEKLY, out_name), 'w', encoding='utf-8').write(all_weeks)
print(f"  weekly/{out_name}")
print(f"done: {len(WEEKS)} week pages, {len(PLOTS)} figures available")
