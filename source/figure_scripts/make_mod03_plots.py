"""Figures 3.1-3.3 for the Week 3 Coordinate Systems page.
Run from the source/ folder:  python figure_scripts/make_mod03_plots.py
Adds three base64 PNGs to plots_data.json (keys mod03w3_*). Needs geopandas, matplotlib."""
import os
import json, base64, warnings, numpy as np, pandas as pd, geopandas as gpd, matplotlib
matplotlib.use("Agg"); warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from io import BytesIO
plt.style.use('seaborn-v0_8-darkgrid'); plt.rcParams['font.size'] = 11
def b64(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, bbox_inches='tight'); buf.seek(0); plt.close(fig)
    return 'data:image/png;base64,' + base64.b64encode(buf.read()).decode()
plots = {}

# ---- snippets from the page (tested here) ----
pt = gpd.GeoSeries([Point(-88.2073, 40.1106)], crs="EPSG:4326")   # Urbana
print("4326:", pt.iloc[0].x, pt.iloc[0].y)
utm = pt.to_crs("EPSG:32616"); print("32616:", round(utm.iloc[0].x,1), round(utm.iloc[0].y,1))
web = pt.to_crs("EPSG:3857");  print("3857:", round(web.iloc[0].x,1), round(web.iloc[0].y,1))
back = utm.to_crs("EPSG:4326"); print("back:", round(back.iloc[0].x,4), round(back.iloc[0].y,4))

samples = pd.DataFrame({"site":["S1","S2","S3","S4","S5","S6","S7","S8"],
    "lon":[-88.237,-88.231,-88.225,-88.236,-88.229,-88.223,-88.234,-88.226],
    "lat":[40.093,40.094,40.092,40.099,40.100,40.098,40.103,40.103]})
pts = gpd.GeoDataFrame(samples, geometry=gpd.points_from_xy(samples.lon, samples.lat), crs="EPSG:4326")
field = gpd.GeoDataFrame({"name":["North field"]}, geometry=[Polygon([(-88.240,40.090),(-88.220,40.090),(-88.220,40.105),(-88.240,40.105)])], crs="EPSG:4326")
print("area deg2:", float(field.area.iloc[0]), " area m2:", round(float(field.to_crs("EPSG:32616").area.iloc[0])), " area 3857 m2:", round(float(field.to_crs("EPSG:3857").area.iloc[0])))
pu = pts.to_crs("EPSG:32616")
print("dist S1-S2 utm:", round(pu.geometry.iloc[0].distance(pu.geometry.iloc[1]),1), " in degrees:", round(pts.geometry.iloc[0].distance(pts.geometry.iloc[1]),5))
naive = gpd.GeoDataFrame(samples, geometry=gpd.points_from_xy(samples.lon, samples.lat))
print("naive crs:", naive.crs); naive = naive.set_crs("EPSG:4326"); print("after set_crs:", naive.crs)
# km per degree
lat = np.linspace(0, 80, 9); km_lon = 111.32*np.cos(np.radians(lat)); print(dict(zip(lat.astype(int), km_lon.round(1))))

# ---- Fig 3.1: same field, degrees vs meters ----
fig, (a0,a1) = plt.subplots(1,2, figsize=(12,5.2))
field.plot(ax=a0, facecolor="none", edgecolor="black", linewidth=2); pts.plot(ax=a0, color="#667eea", edgecolor="black", markersize=90)
a0.set_title("EPSG:4326 — degrees", fontsize=13, fontweight="bold"); a0.set_xlabel("Longitude (°)", fontweight="bold"); a0.set_ylabel("Latitude (°)", fontweight="bold")
fu = field.to_crs("EPSG:32616")
fu.plot(ax=a1, facecolor="none", edgecolor="black", linewidth=2); pu.plot(ax=a1, color="#764ba2", edgecolor="black", markersize=90)
a1.set_title("EPSG:32616 — meters (UTM 16N)", fontsize=13, fontweight="bold"); a1.set_xlabel("Easting (m)", fontweight="bold"); a1.set_ylabel("Northing (m)", fontweight="bold")
a1.ticklabel_format(style="plain", useOffset=False)
for a in (a0,a1): a.set_aspect("equal")
a0.set_xticks([-88.240, -88.235, -88.230, -88.225, -88.220])
a1.set_xticks([394500, 395000, 395500, 396000])
fig.suptitle("Same field, same points — only the numbers on the axes change", fontsize=13, y=1.02)
fig.tight_layout()
plots["mod03w3_degrees_vs_meters"] = b64(fig)

# ---- Fig 3.2: US in three CRS ----
US_STATES = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
try:
    states = gpd.read_file(US_STATES)
except Exception:
    states = gpd.read_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "us-states.json"))  # local copy fallback
cont = states[~states["name"].isin(["Alaska","Hawaii","Puerto Rico"])]
fig, axes = plt.subplots(1,3, figsize=(15,4.8))
for ax, (code, label) in zip(axes, [("EPSG:4326","EPSG:4326 (degrees)\nlooks squashed east-west"),("EPSG:3857","EPSG:3857 (Web Mercator)\nnorth stretched"),("EPSG:5070","EPSG:5070 (Albers equal-area)\nareas correct, curved")]):
    g = cont.to_crs(code); g.plot(ax=ax, facecolor="#c9d1f5", edgecolor="#764ba2", linewidth=0.4)
    ax.set_title(label, fontsize=11, fontweight="bold"); ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
fig.suptitle("The same 48 states in three coordinate systems", fontsize=13, fontweight="bold")
plots["mod03w3_projections"] = b64(fig)

# ---- Fig 3.3: km per degree of longitude ----
fig, ax = plt.subplots(figsize=(9,5))
latf = np.linspace(0, 90, 200); ax.plot(latf, 111.32*np.cos(np.radians(latf)), color="#667eea", linewidth=3)
ax.axhline(111.32, color="#764ba2", linestyle="--", linewidth=2, label="1° of latitude ≈ 111 km everywhere")
ax.scatter([40.1],[111.32*np.cos(np.radians(40.1))], s=120, color="red", zorder=5, edgecolor="black")
ax.annotate("Urbana, IL (40.1°N):\n1° longitude ≈ 85 km", (40.1, 85), xytext=(48, 95), fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("Latitude (°)", fontweight="bold"); ax.set_ylabel("Length of 1° of longitude (km)", fontweight="bold")
ax.set_title("Why degrees are not a unit of distance", fontsize=13, fontweight="bold"); ax.legend(); ax.set_ylim(0,125)
plots["mod03w3_degree_length"] = b64(fig)

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plots_data.json")
d = json.load(open(path)); d.update(plots); json.dump(d, open(path,"w"))
print({k: len(v)//1024 for k,v in plots.items()}, "keys:", len(d))
