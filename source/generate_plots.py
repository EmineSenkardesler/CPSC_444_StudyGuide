#!/usr/bin/env python3
"""Generate educational plots for study guide modules"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from scipy import stats
from io import BytesIO
import base64
import os

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f'data:image/png;base64,{img_base64}'

def generate_module01_plots():
    """Generate plots for Module 01: Foundations"""
    plots = {}

    # 1. Simple Linear Regression
    fig, ax = plt.subplots(figsize=(10, 6))
    np.random.seed(42)
    rainfall = np.array([20, 25, 30, 35, 40, 22, 28, 33, 38, 24])
    yields = 120 + 2*rainfall + np.random.normal(0, 5, 10)

    # Fit line
    slope, intercept, r_value, _, _ = stats.linregress(rainfall, yields)
    line_x = np.linspace(rainfall.min(), rainfall.max(), 100)
    line_y = slope * line_x + intercept

    ax.scatter(rainfall, yields, s=100, alpha=0.6, color='#667eea', edgecolors='black', linewidth=1.5)
    ax.plot(line_x, line_y, 'r-', linewidth=2, label=f'y = {intercept:.1f} + {slope:.2f}x\nR² = {r_value**2:.3f}')
    ax.set_xlabel('Rainfall (inches)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Yield (bushels/acre)', fontsize=12, fontweight='bold')
    ax.set_title('Simple Linear Regression: Yield vs Rainfall', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plots['regression'] = fig_to_base64(fig)

    # 2. Distribution Comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    x = np.linspace(-4, 4, 100)

    # Normal
    axes[0,0].plot(x, stats.norm.pdf(x, 0, 1), 'b-', linewidth=2)
    axes[0,0].fill_between(x, stats.norm.pdf(x, 0, 1), alpha=0.3)
    axes[0,0].set_title('Normal Distribution', fontweight='bold')
    axes[0,0].set_ylabel('Probability Density')
    axes[0,0].grid(True, alpha=0.3)

    # Binomial
    n, p = 20, 0.5
    x_binom = np.arange(0, n+1)
    axes[0,1].bar(x_binom, stats.binom.pmf(x_binom, n, p), color='green', alpha=0.6, edgecolor='black')
    axes[0,1].set_title('Binomial Distribution (n=20, p=0.5)', fontweight='bold')
    axes[0,1].set_ylabel('Probability')
    axes[0,1].grid(True, alpha=0.3)

    # Poisson
    mu = 5
    x_poisson = np.arange(0, 15)
    axes[1,0].bar(x_poisson, stats.poisson.pmf(x_poisson, mu), color='orange', alpha=0.6, edgecolor='black')
    axes[1,0].set_title('Poisson Distribution (λ=5)', fontweight='bold')
    axes[1,0].set_xlabel('Count')
    axes[1,0].set_ylabel('Probability')
    axes[1,0].grid(True, alpha=0.3)

    # Exponential
    x_exp = np.linspace(0, 5, 100)
    axes[1,1].plot(x_exp, stats.expon.pdf(x_exp, scale=1), 'r-', linewidth=2)
    axes[1,1].fill_between(x_exp, stats.expon.pdf(x_exp, scale=1), alpha=0.3, color='red')
    axes[1,1].set_title('Exponential Distribution', fontweight='bold')
    axes[1,1].set_xlabel('Value')
    axes[1,1].set_ylabel('Probability Density')
    axes[1,1].grid(True, alpha=0.3)

    plt.tight_layout()
    plots['distributions'] = fig_to_base64(fig)

    # 3. Q-Q Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Normal data
    normal_data = np.random.normal(0, 1, 100)
    stats.probplot(normal_data, dist="norm", plot=ax1)
    ax1.set_title('Q-Q Plot: Normal Data\n(Points on line = normally distributed)', fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Skewed data
    skewed_data = np.random.exponential(2, 100)
    stats.probplot(skewed_data, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot: Skewed Data\n(Points curve = not normally distributed)', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plots['qqplot'] = fig_to_base64(fig)

    return plots

def generate_module02_plots():
    """Generate plots for Module 02: Statistical Foundations"""
    plots = {}

    # 1. Logistic Regression Sigmoid
    fig, ax = plt.subplots(figsize=(10, 6))
    z = np.linspace(-6, 6, 100)
    sigmoid = 1 / (1 + np.exp(-z))

    ax.plot(z, sigmoid, 'b-', linewidth=3, label='Sigmoid: σ(z) = 1/(1+e⁻ᶻ)')
    ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Decision boundary (0.5)')
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    ax.fill_between(z, 0, sigmoid, where=(z<0), alpha=0.2, color='red', label='Predict: No')
    ax.fill_between(z, sigmoid, 1, where=(z>=0), alpha=0.2, color='green', label='Predict: Yes')
    ax.set_xlabel('z = β₀ + β₁x₁ + β₂x₂ + ...', fontsize=12, fontweight='bold')
    ax.set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
    ax.set_title('Logistic Regression: Sigmoid Function', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.1, 1.1)
    plots['sigmoid'] = fig_to_base64(fig)

    # 2. Confusion Matrix
    fig, ax = plt.subplots(figsize=(8, 6))
    confusion = np.array([[85, 15], [10, 90]])

    im = ax.imshow(confusion, cmap='Blues', aspect='auto')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Predicted: No', 'Predicted: Yes'], fontsize=11)
    ax.set_yticklabels(['Actual: No', 'Actual: Yes'], fontsize=11)

    # Add text annotations
    for i in range(2):
        for j in range(2):
            text = ax.text(j, i, confusion[i, j], ha="center", va="center",
                          color="white" if confusion[i, j] > 50 else "black",
                          fontsize=24, fontweight='bold')

    # Add labels
    ax.text(0, -0.5, 'TN=85\n(Correct)', ha='center', fontsize=10, color='green', fontweight='bold')
    ax.text(1, -0.5, 'FP=15\n(False Alarm)', ha='center', fontsize=10, color='red', fontweight='bold')
    ax.text(0, 1.5, 'FN=10\n(Missed)', ha='center', fontsize=10, color='red', fontweight='bold')
    ax.text(1, 1.5, 'TP=90\n(Correct)', ha='center', fontsize=10, color='green', fontweight='bold')

    accuracy = (85 + 90) / (85 + 15 + 10 + 90)
    ax.set_title(f'Confusion Matrix Example\nAccuracy = {accuracy:.1%}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plots['confusion_matrix'] = fig_to_base64(fig)

    # 3. ROC Curve
    fig, ax = plt.subplots(figsize=(8, 8))

    # Generate sample ROC curve
    np.random.seed(42)
    fpr = np.array([0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0])
    tpr = np.array([0, 0.6, 0.75, 0.85, 0.9, 0.95, 0.98, 1.0])

    auc = np.trapz(tpr, fpr)

    ax.plot(fpr, tpr, 'b-', linewidth=3, label=f'Model (AUC = {auc:.2f})')
    ax.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Random Classifier (AUC = 0.50)')
    ax.fill_between(fpr, 0, tpr, alpha=0.3)
    ax.set_xlabel('False Positive Rate', fontsize=12, fontweight='bold')
    ax.set_ylabel('True Positive Rate', fontsize=12, fontweight='bold')
    ax.set_title('ROC Curve Example', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    plots['roc_curve'] = fig_to_base64(fig)

    return plots

def generate_module03_plots():
    """Generate plots for Module 03: Geospatial Fundamentals"""
    plots = {}

    # 1. Raster vs Vector
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Raster
    raster_data = np.random.rand(10, 10) * 100
    im = ax1.imshow(raster_data, cmap='terrain', aspect='auto')
    ax1.set_title('Raster Data\n(Grid of cells with values)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Column (pixel)')
    ax1.set_ylabel('Row (pixel)')
    plt.colorbar(im, ax=ax1, label='Value')
    ax1.grid(True, alpha=0.3, color='white', linewidth=0.5)

    # Vector
    # Create sample polygons
    ax2.fill([1, 4, 4, 1], [1, 1, 3, 3], alpha=0.5, color='blue', edgecolor='black', linewidth=2, label='Field 1')
    ax2.fill([5, 8, 8, 5], [2, 2, 5, 5], alpha=0.5, color='green', edgecolor='black', linewidth=2, label='Field 2')
    ax2.plot([2, 6], [4, 6], 'r-', linewidth=3, label='Road')
    ax2.scatter([3, 7], [2, 4], s=200, c='red', marker='o', edgecolors='black', linewidth=2, label='Sample Points')
    ax2.set_title('Vector Data\n(Points, lines, polygons)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('X Coordinate')
    ax2.set_ylabel('Y Coordinate')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 9)
    ax2.set_ylim(0, 7)

    plt.tight_layout()
    plots['raster_vector'] = fig_to_base64(fig)

    # 2. Kriging Example
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Sample points
    np.random.seed(42)
    sample_x = np.array([1, 3, 7, 2, 8, 5])
    sample_y = np.array([1, 6, 3, 8, 7, 4])
    sample_values = np.array([45, 75, 55, 80, 70, 60])

    # Plot 1: Sample points
    axes[0].scatter(sample_x, sample_y, c=sample_values, s=200, cmap='RdYlGn',
                    edgecolors='black', linewidth=2, vmin=40, vmax=85)
    for i, val in enumerate(sample_values):
        axes[0].annotate(f'{val}', (sample_x[i], sample_y[i]),
                        xytext=(5, 5), textcoords='offset points', fontweight='bold')
    axes[0].set_title('Step 1: Sample Points\n(Known values)', fontweight='bold')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, 9)
    axes[0].set_ylim(0, 9)

    # Plot 2: Interpolation concept
    axes[1].scatter(sample_x, sample_y, c=sample_values, s=200, cmap='RdYlGn',
                    edgecolors='black', linewidth=2, vmin=40, vmax=85, label='Known')
    axes[1].scatter([4.5], [5], s=300, c='white', marker='X', edgecolors='red', linewidth=3, label='Unknown')
    axes[1].arrow(4.5, 5, -1, 1, head_width=0.3, head_length=0.2, fc='blue', ec='blue', alpha=0.5)
    axes[1].arrow(4.5, 5, 0.5, -1, head_width=0.3, head_length=0.2, fc='blue', ec='blue', alpha=0.5)
    axes[1].set_title('Step 2: Kriging\n(Use nearby points + spatial structure)', fontweight='bold')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(0, 9)
    axes[1].set_ylim(0, 9)

    # Plot 3: Interpolated surface
    grid_x, grid_y = np.meshgrid(np.linspace(0, 9, 50), np.linspace(0, 9, 50))
    # Simple interpolation for visualization
    from scipy.interpolate import Rbf
    rbf = Rbf(sample_x, sample_y, sample_values, function='multiquadric', smooth=2)
    grid_z = rbf(grid_x, grid_y)

    im = axes[2].contourf(grid_x, grid_y, grid_z, levels=15, cmap='RdYlGn', vmin=40, vmax=85)
    axes[2].scatter(sample_x, sample_y, c='black', s=100, marker='x', linewidth=3)
    axes[2].set_title('Step 3: Interpolated Surface\n(Predicted everywhere)', fontweight='bold')
    axes[2].set_xlabel('X')
    axes[2].set_ylabel('Y')
    plt.colorbar(im, ax=axes[2], label='Predicted Value')

    plt.tight_layout()
    plots['kriging_example'] = fig_to_base64(fig)

    # 3. Semivariogram
    fig, ax = plt.subplots(figsize=(10, 6))

    distances = np.linspace(0, 10, 100)
    nugget = 5
    sill = 30
    range_val = 5

    # Spherical model
    gamma = np.where(distances < range_val,
                     nugget + (sill - nugget) * (1.5 * distances/range_val - 0.5 * (distances/range_val)**3),
                     sill)

    ax.plot(distances, gamma, 'b-', linewidth=3, label='Spherical Model')
    ax.axhline(y=sill, color='r', linestyle='--', linewidth=2, label=f'Sill = {sill}')
    ax.axhline(y=nugget, color='g', linestyle='--', linewidth=2, label=f'Nugget = {nugget}')
    ax.axvline(x=range_val, color='orange', linestyle='--', linewidth=2, label=f'Range = {range_val}')

    # Add annotations
    ax.annotate('Nugget\n(measurement error)', xy=(0, nugget), xytext=(1, 10),
                arrowprops=dict(arrowstyle='->', color='green'), fontsize=10, fontweight='bold')
    ax.annotate('Sill\n(max variance)', xy=(7, sill), xytext=(7, 35),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, fontweight='bold')
    ax.annotate('Range\n(correlation distance)', xy=(range_val, 20), xytext=(6, 15),
                arrowprops=dict(arrowstyle='->', color='orange'), fontsize=10, fontweight='bold')

    ax.set_xlabel('Distance (h)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Semivariance γ(h)', fontsize=12, fontweight='bold')
    ax.set_title('Semivariogram Components', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 40)
    plots['semivariogram'] = fig_to_base64(fig)

    return plots

def generate_module04_plots():
    """Generate plots for Module 04: Spatial Statistics"""
    plots = {}

    # 1. Variogram Models Comparison
    fig, ax = plt.subplots(figsize=(12, 7))

    distances = np.linspace(0, 10, 100)
    nugget = 5
    sill = 30
    range_val = 5

    # Spherical
    gamma_sph = np.where(distances < range_val,
                         nugget + (sill - nugget) * (1.5 * distances/range_val - 0.5 * (distances/range_val)**3),
                         sill)

    # Exponential
    gamma_exp = nugget + (sill - nugget) * (1 - np.exp(-3 * distances / range_val))

    # Gaussian
    gamma_gaus = nugget + (sill - nugget) * (1 - np.exp(-3 * (distances / range_val)**2))

    ax.plot(distances, gamma_sph, 'b-', linewidth=3, label='Spherical (most common)')
    ax.plot(distances, gamma_exp, 'r-', linewidth=3, label='Exponential (gradual)')
    ax.plot(distances, gamma_gaus, 'g-', linewidth=3, label='Gaussian (very smooth)')

    ax.axhline(y=sill, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=nugget, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=range_val, color='gray', linestyle='--', alpha=0.5)

    ax.set_xlabel('Distance (h)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Semivariance γ(h)', fontsize=12, fontweight='bold')
    ax.set_title('Comparison of Variogram Models', fontsize=14, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    plots['variogram_models'] = fig_to_base64(fig)

    # 2. Rook vs Queen Contiguity
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Create grid
    grid_size = 5

    # Rook
    for i in range(grid_size):
        for j in range(grid_size):
            if i == 2 and j == 2:
                ax1.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='red', edgecolor='black', linewidth=2))
            elif (i == 2 and j in [1, 3]) or (j == 2 and i in [1, 3]):
                ax1.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='lightblue', edgecolor='black', linewidth=2))
            else:
                ax1.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='white', edgecolor='gray', linewidth=1))

    ax1.set_xlim(0, grid_size)
    ax1.set_ylim(0, grid_size)
    ax1.set_aspect('equal')
    ax1.set_title('Rook Contiguity\n4 neighbors (share edge)', fontsize=12, fontweight='bold')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.text(2.5, -0.7, '🔴 Focal cell\n🔵 Neighbors', ha='center', fontsize=10, fontweight='bold')

    # Queen
    for i in range(grid_size):
        for j in range(grid_size):
            if i == 2 and j == 2:
                ax2.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='red', edgecolor='black', linewidth=2))
            elif abs(i - 2) <= 1 and abs(j - 2) <= 1 and not (i == 2 and j == 2):
                ax2.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='lightgreen', edgecolor='black', linewidth=2))
            else:
                ax2.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='white', edgecolor='gray', linewidth=1))

    ax2.set_xlim(0, grid_size)
    ax2.set_ylim(0, grid_size)
    ax2.set_aspect('equal')
    ax2.set_title('Queen Contiguity\n8 neighbors (share edge or corner)', fontsize=12, fontweight='bold')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.text(2.5, -0.7, '🔴 Focal cell\n🟢 Neighbors', ha='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plots['contiguity'] = fig_to_base64(fig)

    # 3. Spatial Correlogram
    fig, ax = plt.subplots(figsize=(10, 6))

    lags = np.arange(0, 11)
    correlations = np.exp(-lags/3)  # Exponential decay

    ax.bar(lags, correlations, color='steelblue', alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.plot(lags, correlations, 'ro-', linewidth=2, markersize=8)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Moderate correlation')

    ax.set_xlabel('Distance Lag', fontsize=12, fontweight='bold')
    ax.set_ylabel('Spatial Correlation', fontsize=12, fontweight='bold')
    ax.set_title('Spatial Correlogram\n(Shows how correlation decreases with distance)',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(-0.1, 1.1)
    plots['correlogram'] = fig_to_base64(fig)

    return plots

def generate_module05_plots():
    """Generate plots for Module 05: Advanced Regression"""
    plots = {}

    # 1. Ridge vs Lasso Comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    alphas = np.logspace(-2, 3, 50)

    # Ridge coefficients (shrink but don't eliminate)
    ridge_coef1 = 5 / (1 + alphas/10)
    ridge_coef2 = 3 / (1 + alphas/10)
    ridge_coef3 = -2 / (1 + alphas/10)

    axes[0].plot(alphas, ridge_coef1, 'b-', linewidth=2, label='Coefficient 1')
    axes[0].plot(alphas, ridge_coef2, 'r-', linewidth=2, label='Coefficient 2')
    axes[0].plot(alphas, ridge_coef3, 'g-', linewidth=2, label='Coefficient 3')
    axes[0].axhline(y=0, color='black', linestyle='--', alpha=0.3)
    axes[0].set_xscale('log')
    axes[0].set_xlabel('Regularization λ (alpha)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Coefficient Value', fontsize=11, fontweight='bold')
    axes[0].set_title('Ridge (L2): Shrinks all coefficients\n(none become exactly 0)', fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Lasso coefficients (can become exactly 0)
    lasso_coef1 = np.maximum(0, 5 - alphas/5)
    lasso_coef2 = np.maximum(0, 3 - alphas/8)
    lasso_coef3 = np.minimum(0, -2 + alphas/12)

    axes[1].plot(alphas, lasso_coef1, 'b-', linewidth=2, label='Coefficient 1')
    axes[1].plot(alphas, lasso_coef2, 'r-', linewidth=2, label='Coefficient 2')
    axes[1].plot(alphas, lasso_coef3, 'g-', linewidth=2, label='Coefficient 3')
    axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.3)
    axes[1].set_xscale('log')
    axes[1].set_xlabel('Regularization λ (alpha)', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Coefficient Value', fontsize=11, fontweight='bold')
    axes[1].set_title('Lasso (L1): Can eliminate coefficients\n(sets some to exactly 0)', fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plots['ridge_lasso'] = fig_to_base64(fig)

    # 2. GWR Concept
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Global regression
    np.random.seed(42)
    x_west = np.random.uniform(0, 5, 20)
    y_west = 2 + 3*x_west + np.random.normal(0, 1, 20)
    x_east = np.random.uniform(5, 10, 20)
    y_east = 5 + 1*x_east + np.random.normal(0, 1, 20)

    x_all = np.concatenate([x_west, x_east])
    y_all = np.concatenate([y_west, y_east])

    # Global fit
    slope_global, intercept_global = np.polyfit(x_all, y_all, 1)
    x_line = np.linspace(0, 10, 100)
    y_line_global = slope_global * x_line + intercept_global

    axes[0].scatter(x_west, y_west, c='blue', s=50, alpha=0.6, label='West')
    axes[0].scatter(x_east, y_east, c='red', s=50, alpha=0.6, label='East')
    axes[0].plot(x_line, y_line_global, 'k-', linewidth=2, label=f'Global: y={intercept_global:.1f}+{slope_global:.1f}x')
    axes[0].set_title('Regular Regression\n(Same relationship everywhere)', fontweight='bold')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # GWR local fits
    slope_west, intercept_west = np.polyfit(x_west, y_west, 1)
    slope_east, intercept_east = np.polyfit(x_east, y_east, 1)

    y_line_west = slope_west * x_line + intercept_west
    y_line_east = slope_east * x_line + intercept_east

    axes[1].scatter(x_west, y_west, c='blue', s=50, alpha=0.6, label='West')
    axes[1].scatter(x_east, y_east, c='red', s=50, alpha=0.6, label='East')
    axes[1].plot(x_line, y_line_west, 'b-', linewidth=2, label=f'West: slope={slope_west:.1f}')
    axes[1].plot(x_line, y_line_east, 'r-', linewidth=2, label=f'East: slope={slope_east:.1f}')
    axes[1].set_title('GWR\n(Different relationships by location)', fontweight='bold')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Spatial variation in coefficients
    locations = np.linspace(0, 10, 50)
    coefficients = slope_west + (slope_east - slope_west) * (locations / 10)

    axes[2].plot(locations, coefficients, 'g-', linewidth=3)
    axes[2].fill_between(locations, coefficients, alpha=0.3, color='green')
    axes[2].axhline(y=slope_west, color='blue', linestyle='--', label=f'West slope={slope_west:.1f}')
    axes[2].axhline(y=slope_east, color='red', linestyle='--', label=f'East slope={slope_east:.1f}')
    axes[2].set_title('Coefficient Variation\n(Changes across space)', fontweight='bold')
    axes[2].set_xlabel('Location (West → East)')
    axes[2].set_ylabel('Coefficient Value')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plots['gwr_concept'] = fig_to_base64(fig)

    return plots

def generate_module06_plots():
    """Generate plots for Module 06: Mixed Models"""
    plots = {}

    # Random Intercept vs Random Slope
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    np.random.seed(42)
    x = np.linspace(0, 10, 50)

    # Random Intercept (parallel lines)
    base_intercept = 5
    common_slope = 2

    for i, color in enumerate(['blue', 'red', 'green', 'orange']):
        intercept = base_intercept + np.random.normal(0, 2)
        y = intercept + common_slope * x + np.random.normal(0, 0.5, len(x))
        axes[0].plot(x, y, color=color, linewidth=2, alpha=0.7, label=f'Group {i+1}')

    axes[0].set_title('Random Intercept Model\n(Different baselines, same slope)', fontweight='bold')
    axes[0].set_xlabel('X (e.g., Fertilizer)', fontsize=11)
    axes[0].set_ylabel('Y (e.g., Yield)', fontsize=11)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Random Slope (different slopes and intercepts)
    for i, color in enumerate(['blue', 'red', 'green', 'orange']):
        intercept = base_intercept + np.random.normal(0, 2)
        slope = common_slope + np.random.normal(0, 0.8)
        y = intercept + slope * x + np.random.normal(0, 0.5, len(x))
        axes[1].plot(x, y, color=color, linewidth=2, alpha=0.7, label=f'Group {i+1}')

    axes[1].set_title('Random Slope Model\n(Different baselines AND slopes)', fontweight='bold')
    axes[1].set_xlabel('X (e.g., Fertilizer)', fontsize=11)
    axes[1].set_ylabel('Y (e.g., Yield)', fontsize=11)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plots['random_effects'] = fig_to_base64(fig)

    return plots

def generate_module07_plots():
    """Generate plots for Module 07: Machine Learning"""
    plots = {}

    # 1. Decision Boundaries
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Generate sample data
    np.random.seed(42)
    n = 100
    # Class 1
    x1_c1 = np.random.normal(2, 1, n)
    x2_c1 = np.random.normal(2, 1, n)
    # Class 2
    x1_c2 = np.random.normal(5, 1, n)
    x2_c2 = np.random.normal(5, 1, n)

    # Linear decision boundary
    axes[0].scatter(x1_c1, x2_c1, c='blue', s=30, alpha=0.6, label='Class 1')
    axes[0].scatter(x1_c2, x2_c2, c='red', s=30, alpha=0.6, label='Class 2')

    # Draw linear boundary
    x_boundary = np.linspace(0, 7, 100)
    y_boundary = x_boundary
    axes[0].plot(x_boundary, y_boundary, 'k-', linewidth=3, label='Linear Boundary')
    axes[0].fill_between(x_boundary, 0, y_boundary, alpha=0.1, color='blue')
    axes[0].fill_between(x_boundary, y_boundary, 8, alpha=0.1, color='red')

    axes[0].set_title('Linear Decision Boundary\n(Logistic Regression)', fontweight='bold')
    axes[0].set_xlabel('Feature 1')
    axes[0].set_ylabel('Feature 2')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, 7)
    axes[0].set_ylim(0, 7)

    # Non-linear decision boundary
    axes[1].scatter(x1_c1, x2_c1, c='blue', s=30, alpha=0.6, label='Class 1')
    axes[1].scatter(x1_c2, x2_c2, c='red', s=30, alpha=0.6, label='Class 2')

    # Draw non-linear boundary (circular)
    theta = np.linspace(0, 2*np.pi, 100)
    r = 2.5
    x_circle = 3.5 + r * np.cos(theta)
    y_circle = 3.5 + r * np.sin(theta)
    axes[1].plot(x_circle, y_circle, 'k-', linewidth=3, label='Non-linear Boundary')
    axes[1].fill(x_circle, y_circle, alpha=0.1, color='blue')

    axes[1].set_title('Non-linear Decision Boundary\n(Random Forest, Neural Networks)', fontweight='bold')
    axes[1].set_xlabel('Feature 1')
    axes[1].set_ylabel('Feature 2')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(0, 7)
    axes[1].set_ylim(0, 7)

    plt.tight_layout()
    plots['decision_boundaries'] = fig_to_base64(fig)

    # 2. Feature Importance
    fig, ax = plt.subplots(figsize=(10, 6))

    features = ['Rainfall', 'Temperature', 'Nitrogen', 'Phosphorus', 'Potassium',
                'pH', 'Organic Matter', 'Soil Texture']
    importances = [0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01]

    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(features)))
    bars = ax.barh(features, importances, color=colors, edgecolor='black', linewidth=1.5)

    # Add value labels
    for i, (bar, imp) in enumerate(zip(bars, importances)):
        ax.text(imp + 0.01, i, f'{imp:.2f}', va='center', fontweight='bold')

    ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
    ax.set_title('Random Forest: Feature Importance\n(Which variables matter most for prediction?)',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(0, 0.4)

    plt.tight_layout()
    plots['feature_importance'] = fig_to_base64(fig)

    return plots

def main():
    """Generate all plots and save as dictionary"""
    print("Generating plots for all modules...")

    all_plots = {}

    print("\n📊 Module 01 plots...")
    all_plots.update({f'mod01_{k}': v for k, v in generate_module01_plots().items()})

    print("📊 Module 02 plots...")
    all_plots.update({f'mod02_{k}': v for k, v in generate_module02_plots().items()})

    print("📊 Module 03 plots...")
    all_plots.update({f'mod03_{k}': v for k, v in generate_module03_plots().items()})

    print("📊 Module 04 plots...")
    all_plots.update({f'mod04_{k}': v for k, v in generate_module04_plots().items()})

    print("📊 Module 05 plots...")
    all_plots.update({f'mod05_{k}': v for k, v in generate_module05_plots().items()})

    print("📊 Module 06 plots...")
    all_plots.update({f'mod06_{k}': v for k, v in generate_module06_plots().items()})

    print("📊 Module 07 plots...")
    all_plots.update({f'mod07_{k}': v for k, v in generate_module07_plots().items()})

    print(f"\n✓ Generated {len(all_plots)} plots successfully!")

    # Save to file for use by HTML generator
    import json
    output_file = '/home/emine2/cpsc444-study-guide/plots_data.json'
    with open(output_file, 'w') as f:
        json.dump(all_plots, f)

    print(f"✓ Plots data saved to: {output_file}")

    # Calculate total size
    total_size = sum(len(v) for v in all_plots.values())
    print(f"✓ Total plot data size: {total_size/1024:.1f} KB")

    return all_plots

if __name__ == '__main__':
    plots = main()
