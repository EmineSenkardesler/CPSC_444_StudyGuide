# CPSC 444 Study Guide
## Spatial Statistics, Geospatial Analysis & Agricultural Data Science

Welcome to your organized study guide for CPSC 444! This guide reorganizes all course materials into 8 clear learning modules, progressing from basic Python and statistics to advanced machine learning techniques for spatial data.

---

## Quick Start

**New to programming?** Start with [Module 01: Foundations](Module_01_Foundations.md)

**Know Python already?** Jump to [Module 02: Statistical Foundations](Module_02_Statistical_Foundations.md)

**Want a custom path?** Check out the [Study Paths Guide](Study_Paths.md)

---

## What You'll Learn

This course teaches you how to work with spatial data, from understanding basic statistics and Python programming to applying advanced machine learning techniques. You'll learn:

- How to analyze data that has a location component (like farm fields, weather stations, or GPS points)
- Statistical methods specifically designed for spatial data
- Machine learning techniques for predicting outcomes across geographic areas
- Practical applications in agriculture, environmental science, and beyond

---

## Course Modules

### [Module 01: Foundations](Module_01_Foundations.md) ⭐ **Beginner**
**Time**: 3-5 hours | **Prerequisites**: None

Learn Python basics, data types, visualization, and simple statistics. This is your starting point if you're new to Python.

**Key Topics**: Lists, functions, plots, distributions, simple regression

---

### [Module 02: Statistical Foundations](Module_02_Statistical_Foundations.md) ⭐⭐ **Intermediate**
**Time**: 5-7 hours | **Prerequisites**: Module 01

Master regression analysis with multiple predictors and learn how to build models that classify and predict outcomes.

**Key Topics**: Multiple regression, logistic regression, model evaluation, correlation

---

### [Module 03: Geospatial Fundamentals](Module_03_Geospatial_Fundamentals.md) ⭐⭐⭐ **Intermediate**
**Time**: 8-10 hours | **Prerequisites**: Modules 01, 02

Understand spatial data, coordinate systems, and how to fill gaps in spatial measurements using interpolation.

**Key Topics**: Rasters, vectors, coordinate systems, Kriging, spatial sampling

---

### [Module 04: Spatial Statistics](Module_04_Spatial_Statistics.md) ⭐⭐⭐⭐ **Advanced**
**Time**: 10-12 hours | **Prerequisites**: Module 03

Learn how nearby locations influence each other and how to measure spatial patterns in your data.

**Key Topics**: Semivariograms, spatial autocorrelation, nugget/sill/range, contiguity

---

### [Module 05: Advanced Regression](Module_05_Advanced_Regression.md) ⭐⭐⭐⭐ **Advanced**
**Time**: 8-10 hours | **Prerequisites**: Modules 02, 03, 04

Build sophisticated models that prevent overfitting and account for geographic variations in relationships.

**Key Topics**: Lasso, Ridge, Geographically Weighted Regression, hyperparameter tuning

---

### [Module 06: Mixed Models](Module_06_Mixed_Models.md) ⭐⭐⭐⭐⭐ **Advanced**
**Time**: 10-12 hours | **Prerequisites**: Modules 02, 04

Handle complex hierarchical data where observations are grouped (like plots within fields within farms).

**Key Topics**: Fixed vs random effects, hierarchical modeling, BLUP, EM algorithm

---

### [Module 07: Machine Learning](Module_07_Machine_Learning.md) ⭐⭐⭐⭐⭐ **Advanced**
**Time**: 12-15 hours | **Prerequisites**: Modules 02, 05

Apply modern machine learning methods including ensemble models and neural networks to spatial problems.

**Key Topics**: Random Forest, XGBoost, CNNs for spatial data, pattern removal

---

### [Module 08: Specialized Applications](Module_08_Specialized_Applications.md) ⭐⭐⭐⭐⭐ **Expert**
**Time**: 10-15 hours | **Prerequisites**: Multiple modules

See how all these techniques come together in real-world applications like crop modeling and multi-source data analysis.

**Key Topics**: Crop growth models, data fusion, genomics applications

---

## Study Paths

Choose a path based on your background and goals. See [Study_Paths.md](Study_Paths.md) for detailed schedules.

### Path 1: Complete Beginner → Expert
**Time**: 70-90 hours
**Route**: Modules 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8
**Best for**: New to programming or statistics

### Path 2: Python-Proficient Student
**Time**: 50-70 hours
**Route**: Skim Module 1 → Modules 2 → 3 → 4 → 5 → 6 → 7 → 8
**Best for**: Know Python, need stats and spatial skills

### Path 3: GIS/Spatial Focus
**Time**: 40-50 hours
**Route**: Modules 1 → 3 → 4 → 5 (GWR only) → 7 (CNNs only)
**Best for**: Focused on mapping and spatial analysis

### Path 4: Machine Learning Focus
**Time**: 35-45 hours
**Route**: Modules 1 → 2 → 5 → 6 → 7 → 8
**Best for**: Want to apply ML to complex data

---

## Prerequisites & Setup

### Before You Start

You'll need:
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Basic computer literacy (can navigate folders, install software)

### Python Libraries

The course uses these main libraries:
- **Core**: `numpy`, `pandas`, `matplotlib`, `scipy`
- **Geospatial**: `geopandas`, `rasterio`, `shapely`, `pyproj`
- **Kriging**: `pykrige`
- **Machine Learning**: `scikit-learn`, `xgboost`
- **Deep Learning**: `torch` (PyTorch)
- **Visualization**: `plotly`, `seaborn`

Installation tip: Consider using conda to manage these packages:
```bash
conda create -n cpsc444 python=3.10
conda activate cpsc444
conda install -c conda-forge geopandas rasterio scikit-learn xgboost pytorch plotly
```

---

## How to Use This Guide

### 1. Start with Your Module
Each module file includes:
- Clear learning objectives
- Simple explanations with real-world examples
- Links to all relevant notebook files
- Key formulas explained in plain language

### 2. Follow the Examples
Read through the concept explanations first, then work through the linked notebooks to see the concepts in action.

### 3. Check Your Understanding
Every module ends with **Study Checkpoints** - questions to verify you've grasped the key ideas before moving on.

### 4. Practice on Real Data
The repository includes datasets in the `datasets/` folder. Try applying what you've learned to this data.

### 5. Build Projects
As you progress, try combining techniques from multiple modules to solve more complex problems.

---

## Additional Resources

### Quick Reference
See [Quick_Reference.md](Quick_Reference.md) for:
- Formulas at a glance
- Common code patterns
- Library usage guide
- Troubleshooting tips

### Course Repository
Original materials: [cpsc444-F2025 repository](git@github.com:acesillinois/cpsc444-F2025.git)

All notebook paths in this guide reference files in `/tmp/cpsc444-study/`

---

## Learning Tips

1. **Don't rush**: Spatial statistics is complex. It's okay if concepts take time to click.

2. **Run the code yourself**: Reading isn't enough - type it out and see what happens when you change things.

3. **Use the checkpoints**: They're there to help you know when you're ready to move on.

4. **Draw it out**: Spatial concepts often make more sense when sketched on paper.

5. **Connect to reality**: Think about where you see these patterns in the real world (weather, crops, disease spread, etc.).

6. **Ask questions**: Note what confuses you and research it. Understanding the "why" matters.

7. **Review earlier modules**: As you advance, you'll understand earlier concepts more deeply. It's worth revisiting.

---

## Summary Statistics

- **Total Notebooks**: 43
- **Total Modules**: 8
- **Beginner Materials**: 8 files
- **Intermediate Materials**: 12 files
- **Advanced Materials**: 23 files
- **Total Learning Time**: 70-95 hours (complete path)

---

## Getting Help

If something isn't clear:
1. Check the [Quick_Reference.md](Quick_Reference.md)
2. Review prerequisite modules
3. Look for examples in the notebooks
4. Search for the concept online (add "Python" or "spatial statistics" to your search)
5. Try working through a simpler example first

---

## Ready to Start?

Choose your starting point:

- **Never programmed before?** → [Module 01: Foundations](Module_01_Foundations.md)
- **Know Python basics?** → [Module 02: Statistical Foundations](Module_02_Statistical_Foundations.md)
- **Want to plan your route?** → [Study Paths Guide](Study_Paths.md)
- **Need quick reference?** → [Quick Reference](Quick_Reference.md)

Good luck with your studies!

---

*Study guide created for CPSC 444 - Fall 2025*
*Organized to support self-paced learning from foundations to expert-level applications*
