"""Figures 2.4, 2.6, 2.7 for the Week 2 (continued) First Maps page.
Run from the source/ folder:  python figure_scripts/make_mod02b_plots.py
Adds three base64 PNGs to plots_data.json (keys mod02b_*). Needs geopandas, scipy, matplotlib."""
import os, json, base64, numpy as np, pandas as pd, geopandas as gpd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from scipy import stats
from io import BytesIO
plt.style.use('seaborn-v0_8-darkgrid'); plt.rcParams['font.size'] = 11
HERE = os.path.dirname(os.path.abspath(__file__))
PLOTS_JSON = os.path.join(os.path.dirname(HERE), "plots_data.json")

def b64(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, bbox_inches='tight'); buf.seek(0)
    plt.close(fig); return 'data:image/png;base64,' + base64.b64encode(buf.read()).decode()

samples = pd.DataFrame({"site":["S1","S2","S3","S4","S5","S6","S7","S8"],
    "lon":[-88.237,-88.231,-88.225,-88.236,-88.229,-88.223,-88.234,-88.226],
    "lat":[40.093,40.094,40.092,40.099,40.100,40.098,40.103,40.103],
    "yield_bu_ac":[178,185,172,190,196,181,188,175]})
pts = gpd.GeoDataFrame(samples, geometry=gpd.points_from_xy(samples.lon, samples.lat), crs="EPSG:4326")
field = gpd.GeoDataFrame({"name":["North field"]}, geometry=[Polygon([(-88.240,40.090),(-88.220,40.090),(-88.220,40.105),(-88.240,40.105)])], crs="EPSG:4326")

np.random.seed(444)
west, east, south, north = -88.245, -88.215, 40.085, 40.110
ncols, nrows = 60, 50
LON, LAT = np.meshgrid(np.linspace(west,east,ncols), np.linspace(north,south,nrows))
elev = (225 - 12*(LON-west)/(east-west) + 6*(LAT-south)/(north-south) + np.random.normal(0,0.8,(nrows,ncols))).astype("float32")
ci = ((pts.geometry.x - west)/(east-west)*ncols).astype(int).clip(0,ncols-1)
ri = ((north - pts.geometry.y)/(north-south)*nrows).astype(int).clip(0,nrows-1)
pts["elev_m"] = elev[ri, ci]
fit = stats.linregress(pts.elev_m, pts.yield_bu_ac)
pts["resid"] = pts.yield_bu_ac - (fit.intercept + fit.slope*pts.elev_m)

plots = {}
# Fig 2.4: table -> map
fig, (a0, a1) = plt.subplots(1, 2, figsize=(12, 5.5), gridspec_kw={"width_ratios":[1,1.3]})
a0.axis("off")
tbl = a0.table(cellText=samples.values, colLabels=["site","lon","lat","yield (bu/ac)"], loc="center", cellLoc="center")
tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1, 1.6)
for (r,c),cell in tbl.get_celld().items():
    if r == 0: cell.set_facecolor("#667eea"); cell.set_text_props(color="white", fontweight="bold")
    elif c in (1,2): cell.set_facecolor("#eef0fb")
a0.set_title("The same data as a table\n(lon/lat columns highlighted)", fontsize=13, fontweight="bold")
field.plot(ax=a1, facecolor="none", edgecolor="black", linewidth=2)
pts.plot(ax=a1, column="yield_bu_ac", cmap="YlGn", legend=True, markersize=160, edgecolor="black", legend_kwds={"label":"Yield (bu/ac)"})
for x,y,s in zip(pts.geometry.x, pts.geometry.y, pts.site):
    a1.annotate(s,(x,y),xytext=(6,6),textcoords="offset points", fontsize=10)
a1.set_title("...and as a map (vector points + polygon)", fontsize=13, fontweight="bold")
a1.set_xlabel("Longitude", fontweight="bold"); a1.set_ylabel("Latitude", fontweight="bold")
plots["mod02b_table_to_map"] = b64(fig)

# Fig 2.6: three-layer overlay
fig, ax = plt.subplots(figsize=(9, 7))
im = ax.imshow(elev, cmap="terrain", extent=[west,east,south,north])
plt.colorbar(im, ax=ax, label="Elevation (m)", shrink=0.8)
field.plot(ax=ax, facecolor="none", edgecolor="white", linewidth=2.5)
pts.plot(ax=ax, column="yield_bu_ac", cmap="YlGn", edgecolor="black", markersize=160, legend=True, legend_kwds={"label":"Yield (bu/ac)", "shrink":0.8})
ax.set_title("Three layers on one map: raster (elevation) + polygon (field) + points (samples)", fontsize=13, fontweight="bold")
ax.set_xlabel("Longitude", fontweight="bold"); ax.set_ylabel("Latitude", fontweight="bold"); ax.grid(False)
plots["mod02b_overlay"] = b64(fig)

# Fig 2.7: regression + residual map
fig, (a0, a1) = plt.subplots(1, 2, figsize=(13, 5.5))
a0.scatter(pts.elev_m, pts.yield_bu_ac, s=110, color="#667eea", edgecolors="black", linewidth=1.5)
xs = np.linspace(pts.elev_m.min()-0.5, pts.elev_m.max()+0.5, 50)
a0.plot(xs, fit.intercept + fit.slope*xs, "r-", linewidth=2, label=f"y = {fit.intercept:.0f} + {fit.slope:.2f}x\nR² = {fit.rvalue**2:.2f}, p = {fit.pvalue:.2f}")
for x,y,s in zip(pts.elev_m, pts.yield_bu_ac, pts.site): a0.annotate(s,(x,y),xytext=(6,4),textcoords="offset points", fontsize=9)
a0.set_xlabel("Elevation at site (m)", fontweight="bold"); a0.set_ylabel("Yield (bu/ac)", fontweight="bold")
a0.set_title("Week 2 view: yield vs elevation", fontsize=13, fontweight="bold"); a0.legend()
field.plot(ax=a1, facecolor="none", edgecolor="black", linewidth=2)
pts.plot(ax=a1, column="resid", cmap="RdBu", vmin=-12, vmax=12, legend=True, markersize=200, edgecolor="black", legend_kwds={"label":"Residual (bu/ac)"})
for x,y,r in zip(pts.geometry.x, pts.geometry.y, pts.resid): a1.annotate(f"{r:+.0f}",(x,y),xytext=(8,6),textcoords="offset points", fontsize=10)
a1.set_title("Map view: where the regression is wrong", fontsize=13, fontweight="bold")
a1.set_xlabel("Longitude", fontweight="bold"); a1.set_ylabel("Latitude", fontweight="bold")
plots["mod02b_regression_residuals"] = b64(fig)

data = json.load(open(PLOTS_JSON)); data.update(plots); json.dump(data, open(PLOTS_JSON, "w"))
print("updated", PLOTS_JSON, "with", list(plots))
