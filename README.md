# CPSC 444 — Study Guide & Weekly Pages (Fall 2026)

Teaching materials for **CPSC 444: Spatial Statistics, Geospatial Analysis & Agricultural Data Science** (University of Illinois). Everything here is written in Markdown and compiled into self-contained HTML pages (figures embedded, no server needed) that can be opened in any browser or posted on Canvas.

## Two guides, one source

| What | File to open | Built from | Built by |
|---|---|---|---|
| **Weekly guide** (on-the-go) | `weekly/CPSC444_Weekly_Guide.html` | `source/Module_*.md` for the weeks taught so far | `source/generate_week2_html.py` |
| **Full guide** (reference) | `full_guide/CPSC444_Study_Guide_with_Graphics.html` | all `source/Module_01…09.md` + `Quick_Reference.md` + `Study_Paths.md` | `source/build_full_guide.py` |

- The **full guide** is the complete 8-module reorganisation of last year's course material. It is the reference; it does not change week to week.
- The **weekly guide** is what students actually get during the semester. It is *not* finished class notes — it is a running document that grows by one page each week, written to match what was covered in that week's module. Pages can be short, simple and example-driven, and they are edited as the course moves. Both guides share the same style, the same generator and the same figure store, so a page written for the weekly guide can later be folded into the full guide.

## The four pages so far (weekly guide)

| Sidebar entry | Page heading | Covers | Source file |
|---|---|---|---|
| Module 01 · Week 1 (24–28 Aug) | Week 1: Foundations | Python basics, plotting, summary statistics, distributions, simple regression | `source/Module_01_Foundations.md` |
| M.01 · Week 2 (31 Aug–4 Sep) | Week 2: Statistical Foundations | Multiple & logistic regression, model evaluation, the five regression assumptions | `source/Module_02_Statistical_Foundations.md` |
| M.02 · Week 2 (cont.) | Week 2 (continued): First Maps | Vector vs raster, GeoDataFrames, polygons, first CRS contact, GeoTIFFs, extracting raster values at points and mapping regression residuals | `source/Module_02b_First_Maps.md` |
| M.03 · Week 3 (7–11 Sep) | Week 3: Coordinate Systems & Transformations | Geographic vs projected CRS, EPSG codes, `.to_crs()` vs `.set_crs()`, what changes when you convert, reprojecting rasters | `source/Module_03_Week3_Coordinate_Systems.md` |

How they connect: Weeks 1–2 are tables of numbers and ordinary regression. "First Maps" adds longitude/latitude to those same tables and ends by showing that regression residuals cluster in space — the reason spatial statistics exists. Week 3 explains the one thing First Maps had to hand-wave (the CRS) so that distances and areas mean something before sampling and Kriging (Module 03 of the full guide) begin.

## Where to find what — and what to edit

```
CPSC_444_StudyGuide/
├── README.md                  ← this file
├── weekly/                    OUTPUT + hand-outs for the semester in progress
│   ├── CPSC444_Weekly_Guide.html      the 4-page weekly guide (compiled; do not edit by hand)
│   └── CPSC444_Week2_FirstMaps.ipynb  Colab notebook for the First Maps class (exercises + Think-Pair-Share)
├── full_guide/                OUTPUT
│   └── CPSC444_Study_Guide_with_Graphics.html   the full 8-module reference (compiled; do not edit by hand)
├── source/                    EVERYTHING YOU EDIT
│   ├── Module_01_Foundations.md … Module_09_ANOVA.md   module text (one file = one page)
│   ├── Module_02b_First_Maps.md, Module_03_Week3_Coordinate_Systems.md   weekly-only pages
│   ├── Quick_Reference.md, Study_Paths.md, README.md    extra pages of the full guide
│   ├── plots_data.json        all figures as base64 PNGs, keyed by name (e.g. mod02b_overlay)
│   ├── generate_html_with_plots.py   the Markdown→HTML converter + page template (shared)
│   ├── generate_week2_html.py        builds weekly/  (choose pages, headings, figure placement)
│   ├── build_full_guide.py           builds full_guide/
│   ├── generate_plots.py             regenerates the original full-guide figures
│   └── figure_scripts/               scripts that made the weekly-page figures (mod02b_*, mod03w3_*)
└── ta_notes/                  TA-facing lesson scripts (timed outline, talking points, cheat sheets) — not published to students
```

### I want to…

- **Fix a typo or explain something better on a page** → edit the matching `source/Module_*.md`, then rebuild (below). Never edit the `.html` files; they are overwritten on every build.
- **Add next week's page** → write `source/Module_XX_WeekN_<topic>.md` following the structure of the existing pages (Overview → Learning Objectives → Core Concepts → Course Materials → Key Commands/Formulas → Study Checkpoints → Common Mistakes → Tips → Next Steps), add one tuple to `MODULES` in `source/generate_week2_html.py` (page id, file name, sidebar label), rebuild.
- **Add or replace a figure** → write a small script in `source/figure_scripts/` that saves a base64 PNG into `plots_data.json` under a new key, then add a `PLOT_MARKERS` entry in `generate_week2_html.py` giving the exact heading the figure should appear under. See `figure_scripts/make_mod03_plots.py` for a complete example.
- **Change the look (colours, sidebar, fonts)** → the CSS lives in the template string inside `source/generate_html_with_plots.py`; it is shared by both guides.
- **Change a sidebar label or a page heading** → the `MODULES` list and the heading-override dictionary at the top of `source/generate_week2_html.py`.
- **Update the class notebook** → edit `weekly/CPSC444_Week2_FirstMaps.ipynb` directly in Colab and download it back here.

### Rebuild

```bash
cd source
python generate_week2_html.py     # -> ../weekly/CPSC444_Weekly_Guide.html
python build_full_guide.py        # -> ../full_guide/CPSC444_Study_Guide_with_Graphics.html
```

Building needs only Python 3 (no packages). Regenerating figures or running the notebook code needs `geopandas`, `rasterio`, `scipy`, `matplotlib`.

### Markdown rules the converter understands

The converter in `generate_html_with_plots.py` is deliberately small. Use: `#`–`####` headings, `**bold**`, `` `code` ``, fenced code blocks, `- ` bullet lists, `- [ ]` checklists, `[text](link)`, `---` rules, and raw `<details><summary>` blocks for click-to-reveal answers. It does **not** render tables, `*italics*`, `>` quotes or numbered lists (they become plain paragraphs) — write those as bullets or code blocks instead.

## Course repository

Original notebooks referenced from the pages: [acesillinois/cpsc444-F2025](https://github.com/acesillinois/cpsc444-F2025).
