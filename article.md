---
author: "Kyle Jones"
date_published: "October 28, 2025"
date_exported_from_medium: "November 10, 2025"
canonical_link: "https://medium.com/@kyle-t-jones/mapping-right-of-way-for-pipeline-management-looking-at-vegetation-patterns-with-clustering-bf4e2614b24a"
---

# Mapping Right-of-Way for Pipeline Management Looking at Vegetation Patterns with Clustering A pipeline operator receives a vegetation management report for 150 km
of right-of-way (ROW). The report lists 47 tiles where NDVI...

### Mapping Right-of-Way for Pipeline Management Looking at Vegetation Patterns with Clustering 

A pipeline operator receives a vegetation management report for 150 km of right-of-way (ROW). The report lists 47 tiles where NDVI (vegetation index) exceeds 0.7. Management asks: "Which areas need trimming first?"

The NDVI threshold doesn't answer this. A tile with NDVI=0.75 could be stable forest that's been there for decades, or it could be recent overgrowth encroaching on the pipeline. A tile with NDVI=0.65 might be below the threshold but showing rapid vegetation increase --- a leading indicator of future problems.

Single-variable thresholds treat all high-NDVI tiles identically. They don't capture spatial context, temporal trends, or multivariate patterns (vegetation + thermal + soil disturbance).


Hierarchical clustering solves this. By grouping satellite tiles based on multiple features --- not just NDVI --- it reveals natural environmental zones that map to physical conditions: stable vegetation, recent disturbance, bare soil, construction activity. This article demonstrates a working implementation using Sentinel-2 imagery, Apache Spark, and Databricks Mosaic.

### Point-Based Thresholds vs. Spatial Patterns
Let's consider two scenarios.

Scenario 1: Two tiles both have NDVI = 0.70:

- Tile A: Dense grassland, NDVI stable at 0.70 for 5 years, low texture variance.
- Tile B: Mixed shrubs, NDVI increased from 0.45 to 0.70 in 6 months, high texture variance.

A threshold-based system treats them identically. In reality, Tile B needs immediate vegetation management while Tile A is stable.

Scenario 2: Three tiles all have NDVI \< 0.3 (below "overgrowth" threshold):

- Tile C: Bare soil from recent ROW clearing (planned maintenance).
- Tile D: Exposed soil from third-party excavation (encroachment risk).
- Tile E: Natural desert vegetation (stable, no action needed).

All three are below the threshold, but root causes differ. Treating them uniformly wastes resources or misses critical risks.

Hierarchical clustering identifies groups of tiles with similar multivariate signatures using features like NDVI mean/std, texture, thermal anomaly, and bare soil fraction. The result: natural environmental zones that inform:

- Patrol prioritization: High-risk zones (disturbed soil, thermal anomalies) get weekly drone surveys; stable zones get quarterly patrols.
- Vegetation management: Clusters with increasing NDVI trend get scheduled trimming; stable clusters get extended intervals.
- Encroachment detection: Clusters showing bare soil + thermal anomalies flag potential construction activity.

### Sentinel-2 with Databricks Mosaic
Mosaic enables distributed geospatial processing on Databricks. The workflow ingests Sentinel-2 GeoTIFFs from cloud storage, computes NDVI per tile using the formula NDVI = (NIR --- Red) / (NIR + Red), and extracts additional features including texture metrics via Gray-Level Co-occurrence Matrix (GLCM) and bare soil fraction (NDVI \< 0.2).

*(See Implementation Section 1--3 for setup, ingestion, and feature extraction code)*
### Feature Engineering 

Features are normalized using StandardScaler before clustering to ensure equal weighting. Without normalization, texture GLCM (range 0--50+) would dominate distance metrics over NDVI (range 0--1).

Features used:

- `ndvi_mean`: Average vegetation index
- `ndvi_std`: Vegetation variability
- `texture_glcm`: Spatial texture from co-occurrence matrix
- `thermal_anomaly_score`: Temperature deviation from baseline
- `bare_soil_fraction`: Proportion of bare ground

*(See Implementation Section 4 for normalization code)*

### Hierarchical Clustering
Ward linkage is used to minimize within-cluster variance. The dendrogram visualization shows how tiles merge hierarchically, enabling informed selection of cluster count. Cutting at height=4 yields 5 distinct environmental zones.


Interpreting the dendrogram:

- Y-axis (linkage distance): Height at which clusters merge. Larger values = more dissimilar.
- Horizontal lines: Represent merges.
- Color coding: Each color represents a final cluster at the chosen cut height.

After clustering, cluster profiles are computed showing the mean feature values for each group.

### Cluster Interpretation and Operational Actions
### Cluster 0: "Dense, Stable Vegetation"
- Characteristics: High NDVI (0.72), high texture (forest), low bare soil.
- Physical meaning: Mature forest or dense grassland, stable over time.
- Action: Standard quarterly patrol. Extend vegetation management interval to 18 months.

### Cluster 1: "Bare or Disturbed Ground"
- Characteristics: Very low NDVI (0.18), very high bare soil (0.72), elevated thermal anomaly.
- Physical meaning: Recent ROW clearing, construction, or natural erosion.
- Action: Immediate inspection. Verify if disturbance is planned (ROW maintenance) or unplanned (third-party excavation). If unplanned, dispatch ground crew within 24 hours.

### Cluster 2: "Moderate Vegetation, Mixed Cover"
- Characteristics: Mid-range NDVI (0.45), moderate texture, moderate bare soil.
- Physical meaning: Grassland with patches of exposed soil, typical of semi-arid regions.
- Action: Standard patrol. Monitor for NDVI trends. If NDVI increases above 0.6 in next quarter, schedule trimming.

### Cluster 3: "Healthy Vegetation, High Texture"
- Characteristics: Moderate-high NDVI (0.55), high texture, low bare soil.
- Physical meaning: Mixed shrubs and trees, good vegetation health.
- Action: Quarterly patrol. No immediate action unless NDVI exceeds 0.7 (encroachment risk).

### Cluster 4: "Thermal Anomaly + Exposed Soil"
- Characteristics: Low NDVI (0.32), high bare soil (0.58), high thermal anomaly (0.42).
- Physical meaning: Possible construction equipment, recent excavation, or fire scar.
- Action: URGENT: Encroachment alert. Dispatch aerial drone within 48 hours. Cross-reference with permit database. If no permit, issue stop-work order.

### Spatial Visualization
Cluster assignments are mapped along the ROW corridor, revealing spatial patterns. Dense vegetation (Cluster 0) dominates certain sections, while disturbed ground (Cluster 1) and thermal anomalies (Cluster 4) concentrate in specific locations requiring immediate attention.


Spatial insights:

- Cluster 1 (Bare/Disturbed): Concentrated at km 45--57 and km 102--107. Cross-reference with construction permits.
- Cluster 4 (Thermal Anomaly): 5 tiles at km 102--107. Aerial drone patrol identified bulldozer within 50m of pipeline (encroachment confirmed).
- Cluster 0 (Dense Veg): Dominates km 0--40 and km 120--150. These zones can extend patrol interval from monthly to quarterly, saving \$15K/year in patrol costs.

Interactive maps created with Databricks Mosaic allow operators to click on tiles, filter by cluster ID, and overlay with pipeline centerline and recent inspection reports.

*(See Implementation Section 7--8 for spatial visualization and Mosaic mapping code)*
### Temporal Analysis: Tracking Cluster Migration 

A tile's cluster assignment can change over time as conditions evolve:

- Vegetation regrowth after clearing (Cluster 1 → Cluster 2 → Cluster 3)
- New construction (Cluster 0 → Cluster 4)
- Seasonal vegetation cycles (Cluster 2 ↔ Cluster 3)

Versioned Delta tables track cluster history, enabling detection of high-risk transitions. When tiles move from stable vegetation (Cluster 0) to disturbed ground (Cluster 1 or 4), automatic alerts trigger emergency patrols.

Operational alert: If 3+ tiles show this transition in the same 5 km stretch, trigger emergency patrol.

*(See Implementation Section 9--10 for temporal tracking SQL)*

### So What?
Clustering helps us move beyond normal NDVI thresholds. It reveals natural environmental zones using multiple features, not just vegetation index. Dendrograms show us a visual hierarchy of how tiles merge, enabling informed choice of cluster count.

We can use this approach to identify high-risk clusters (disturbed soil, thermal anomalies) and give those intensive monitoring; stable clusters get extended intervals. We can link thermal anomaly + bare soil signature to identif construction activity before it impacts the pipeline.
### Implementation 

```python
from pyspark.sql import SparkSession
import mosaic as mos

spark = SparkSession.builder.getOrCreate()
mos.enable_mosaic(spark, dbutils)
mos.enable_gdal(spark)  # For raster support
```

### Section 2: Ingest Sentinel-2 Tiles
```python
# Load Sentinel-2 GeoTIFFs from cloud storage
df_rasters = spark.read.format('gdal') \
    .option('raster_storage', 'dbfs:/sentinel2/ROW_tiles/') \
    .load()
df_rasters.createOrReplaceTempView('sentinel2_raw')
```

### Section 3: Compute NDVI and Features
NDVI Computation:

``` 
CREATE OR REPLACE TABLE silver.row_tile_ndvi AS
SELECT
    tile_id,
    ST_Area(geometry) AS tile_area_m2,
    AVG((band_nir - band_red) / (band_nir + band_red)) AS ndvi_mean,
    STDDEV((band_nir - band_red) / (band_nir + band_red)) AS ndvi_std,
    PERCENTILE((band_nir - band_red) / (band_nir + band_red), 0.95) AS ndvi_p95
FROM sentinel2_raw
GROUP BY tile_id, geometry;
```

Texture Metrics (GLCM):

```python
from pyspark.sql.functions import udf
from skimage.feature import graycomatrix, graycoprops
import numpy as np

@udf('double')
def compute_texture_glcm(nir_band):
    """Compute GLCM contrast metric from NIR band."""
    nir_array = np.array(nir_band).reshape(100, 100)
    nir_normalized = ((nir_array - nir_array.min()) / (nir_array.max() - nir_array.min()) * 255).astype(np.uint8)
    
    glcm = graycomatrix(nir_normalized, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    return float(contrast)
df_texture = df_rasters.withColumn('texture_glcm', compute_texture_glcm('band_nir'))
```

Bare Soil Fraction:

``` 
df_features = spark.sql("""
SELECT
    tile_id,
    ndvi_mean,
    ndvi_std,
    SUM(CASE WHEN ndvi < 0.2 THEN 1 ELSE 0 END) / COUNT(*) AS bare_soil_fraction
FROM (
    SELECT tile_id, (band_nir - band_red) / (band_nir + band_red) AS ndvi
    FROM sentinel2_raw
)
GROUP BY tile_id, ndvi_mean, ndvi_std
""")
```

Synthetic Demo Data:

```python
import pandas as pd
import numpy as np

np.random.seed(9)
N_tiles = 150
df_row = pd.DataFrame({
    'tile_id': range(1, N_tiles + 1),
    'chainage_km': np.linspace(0, 150, N_tiles),
    'longitude': np.random.uniform(-110.5, -109.5, N_tiles),
    'latitude': np.random.uniform(35.0, 36.0, N_tiles),
    'ndvi_mean': np.random.uniform(0.1, 0.8, N_tiles),
    'ndvi_std': np.random.uniform(0.01, 0.2, N_tiles),
    'texture_glcm': np.random.uniform(0.05, 0.5, N_tiles),
    'thermal_anomaly_score': np.random.normal(0, 0.3, N_tiles),
    'bare_soil_fraction': np.random.uniform(0, 0.7, N_tiles)
})
# Create realistic patterns
# Cluster 0: Dense vegetation (forest)
forest_indices = np.random.choice(N_tiles, size=40, replace=False)
df_row.loc[forest_indices, 'ndvi_mean'] = np.random.uniform(0.65, 0.80, 40)
df_row.loc[forest_indices, 'ndvi_std'] = np.random.uniform(0.10, 0.20, 40)
df_row.loc[forest_indices, 'bare_soil_fraction'] = np.random.uniform(0.0, 0.10, 40)
# Cluster 1: Bare soil (recent clearing or disturbance)
bare_indices = np.random.choice([i for i in range(N_tiles) if i not in forest_indices], size=25, replace=False)
df_row.loc[bare_indices, 'ndvi_mean'] = np.random.uniform(0.1, 0.25, 25)
df_row.loc[bare_indices, 'bare_soil_fraction'] = np.random.uniform(0.60, 0.85, 25)
df_row.loc[bare_indices, 'thermal_anomaly_score'] = np.random.uniform(0.3, 0.8, 25)
```

### Section 4: Feature Normalization
```python
from sklearn.preprocessing import StandardScaler

features = ['ndvi_mean', 'ndvi_std', 'texture_glcm', 
            'thermal_anomaly_score', 'bare_soil_fraction']
X = df_row[features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Feature statistics:")
print(pd.DataFrame(X_scaled, columns=features).describe())
```

### Section 5: Hierarchical Clustering
```python
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# Ward linkage minimizes within-cluster variance
Z = linkage(X_scaled, method='ward')
# Visualize dendrogram
plt.rcParams['font.family'] = 'serif'
fig, ax = plt.subplots(figsize=(12, 5))
dendrogram(Z, ax=ax, truncate_mode='level', p=6, color_threshold=4,
           above_threshold_color='gray', no_labels=True)
ax.set_xlabel('Tile Index (sorted by similarity)', fontsize=11)
ax.set_ylabel('Linkage Distance', fontsize=11)
ax.set_title('Right-of-Way Environmental Clusters Dendrogram', fontsize=12, pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 5))
ax.spines['bottom'].set_position(('outward', 5))
plt.tight_layout()
plt.savefig('row_vegetation_dendrogram.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Section 6: Assign Cluster Labels
```python
from sklearn.cluster import AgglomerativeClustering

n_clusters = 5
clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
df_row['cluster_id'] = clustering.fit_predict(X_scaled)
# Compute cluster profiles
cluster_profiles = df_row.groupby('cluster_id')[features].mean()
cluster_counts = df_row.groupby('cluster_id').size()
print("\nCluster Profiles:")
print(cluster_profiles.round(3))
print("\nCluster Sizes:")
print(cluster_counts)
```

### Section 7: Spatial Visualization
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 4))
colors_clusters = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#e67e22']
cluster_names = ['Dense Veg', 'Bare/Disturbed', 'Mixed Cover', 'Healthy', 'Thermal Anomaly']
for i in range(n_clusters):
    cluster_data = df_row[df_row['cluster_id'] == i]
    ax.scatter(cluster_data['chainage_km'], cluster_data['ndvi_mean'],
               c=colors_clusters[i], label=f'C{i}: {cluster_names[i]}',
               s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_xlabel('Chainage (km)', fontsize=11)
ax.set_ylabel('NDVI (0-1)', fontsize=11)
ax.set_title('ROW Vegetation Clusters by Location', fontsize=12, pad=15)
ax.legend(loc='upper left', frameon=False, fontsize=9, ncol=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 5))
ax.spines['bottom'].set_position(('outward', 5))
plt.tight_layout()
plt.savefig('row_clusters_spatial.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Section 8: Interactive Mosaic Map
```python
import mosaic as mos

# Convert Pandas to Spark DataFrame
df_spark = spark.createDataFrame(df_row)
# Create geometries from coordinates
df_spark = df_spark.selectExpr(
    '*',
    'ST_Point(longitude, latitude) AS geometry'
)
# Save to Delta Gold table
df_spark.write.mode('overwrite').saveAsTable('gold.row_clusters')
# Visualize with Mosaic
df_map = spark.table('gold.row_clusters')
mos.display(df_map, geometry_col='geometry', color='cluster_id', 
            title='ROW Environmental Clusters', 
            legend_title='Cluster ID')
```

### Section 9: Versioned Delta Table for Temporal Tracking
``` 
CREATE OR REPLACE TABLE gold.row_cluster_history (
    tile_id INT,
    cluster_id INT,
    clustering_date DATE,
    ndvi_mean DOUBLE,
    bare_soil_fraction DOUBLE
) USING DELTA
PARTITIONED BY (clustering_date);
```

### Section 10: Detecting High-Risk Transitions
```python
-- Find tiles that moved from stable vegetation to disturbed ground
WITH transitions AS (
    SELECT
        curr.tile_id,
        curr.chainage_km,
        prev.cluster_id AS prev_cluster,
        curr.cluster_id AS curr_cluster,
        curr.ndvi_mean - prev.ndvi_mean AS ndvi_change
    FROM gold.row_cluster_history curr
    JOIN gold.row_cluster_history prev
      ON curr.tile_id = prev.tile_id
      AND prev.clustering_date = DATE_SUB(curr.clustering_date, 30)
    WHERE curr.clustering_date = CURRENT_DATE()
)
SELECT * FROM transitions
WHERE prev_cluster = 0 AND curr_cluster IN (1, 4)  -- Healthy → Disturbed/Thermal
ORDER BY ndvi_change ASC;
```

### Section 11: Automated Work Order Generation
``` 
# Databricks Job: Run weekly
high_risk_tiles = spark.sql("""
SELECT tile_id, chainage_km, cluster_id, ndvi_mean
FROM gold.row_clusters
WHERE cluster_id IN (1, 4)  -- Disturbed or Thermal Anomaly
  AND last_patrol_date < DATE_SUB(CURRENT_DATE(), 7)
""")

if high_risk_tiles.count() > 0:
    # Generate work orders in CMMS
    work_orders = high_risk_tiles.toPandas().to_dict('records')
    for wo in work_orders:
        dbutils.notebook.run('/WorkOrders/create_patrol_order', 60, wo)
```

### Notebook
```python
# Databricks Notebook: ROW Vegetation Clustering
# Prerequisites:
# 1. Sentinel-2 GeoTIFFs in dbfs:/sentinel2/ROW_tiles/
# 2. Mosaic enabled on cluster


# COMMAND ----------
# Setup
%pip install -q scipy scikit-learn matplotlib pandas
dbutils.library.restartPython()
# COMMAND ----------
# Import libraries
from pyspark.sql import SparkSession
import mosaic as mos
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
spark = SparkSession.builder.getOrCreate()
mos.enable_mosaic(spark, dbutils)
# COMMAND ----------
# For demo: use synthetic data
np.random.seed(9)
N = 150
data = {
    'tile_id': range(1, N + 1),
    'chainage_km': np.linspace(0, 150, N),
    'longitude': np.random.uniform(-110.5, -109.5, N),
    'latitude': np.random.uniform(35.0, 36.0, N),
    'ndvi_mean': np.random.uniform(0.1, 0.8, N),
    'ndvi_std': np.random.uniform(0.01, 0.2, N),
    'texture_glcm': np.random.uniform(0.05, 0.5, N),
    'thermal_anomaly_score': np.random.normal(0, 0.3, N),
    'bare_soil_fraction': np.random.uniform(0, 0.7, N)
}
df_row = pd.DataFrame(data)
print(f'Loaded {len(df_row)} tiles')
# COMMAND ----------
# Normalize features
features = ['ndvi_mean', 'ndvi_std', 'texture_glcm', 
            'thermal_anomaly_score', 'bare_soil_fraction']
X = df_row[features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print('✓ Features normalized')
# COMMAND ----------
# Hierarchical clustering
Z = linkage(X_scaled, method='ward')
print('✓ Linkage computed')
# COMMAND ----------
# Dendrogram
plt.rcParams['font.family'] = 'serif'
fig, ax = plt.subplots(figsize=(12, 5))
dendrogram(Z, ax=ax, truncate_mode='level', p=6, color_threshold=4,
           above_threshold_color='gray', no_labels=True)
ax.set_xlabel('Tile Index', fontsize=11)
ax.set_ylabel('Linkage Distance', fontsize=11)
ax.set_title('ROW Environmental Clusters', fontsize=12, pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 5))
ax.spines['bottom'].set_position(('outward', 5))
plt.tight_layout()
plt.savefig('/dbfs/FileStore/row_dendrogram.png', dpi=300, bbox_inches='tight')
plt.show()
print('✓ Dendrogram saved')
# COMMAND ----------
# Assign clusters
n_clusters = 5
clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
df_row['cluster_id'] = clustering.fit_predict(X_scaled)
cluster_profiles = df_row.groupby('cluster_id')[features].mean()
print('\nCluster Profiles:')
print(cluster_profiles.round(3))
# COMMAND ----------
# Save to Delta
df_spark = spark.createDataFrame(df_row)
df_spark = df_spark.selectExpr('*', 'ST_Point(longitude, latitude) AS geometry')
df_spark.write.mode('overwrite').saveAsTable('gold.row_clusters')
print('✓ Saved to gold.row_clusters')
# COMMAND ----------
# Spatial visualization
fig, ax = plt.subplots(figsize=(12, 4))
colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#e67e22']
names = ['Dense Veg', 'Bare/Disturbed', 'Mixed', 'Healthy', 'Thermal']
for i in range(n_clusters):
    data = df_row[df_row['cluster_id'] == i]
    ax.scatter(data['chainage_km'], data['ndvi_mean'],
               c=colors[i], label=f'C{i}: {names[i]}',
               s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_xlabel('Chainage (km)', fontsize=11)
ax.set_ylabel('NDVI', fontsize=11)
ax.set_title('ROW Clusters by Location', fontsize=12, pad=15)
ax.legend(loc='upper left', frameon=False, fontsize=9, ncol=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 5))
ax.spines['bottom'].set_position(('outward', 5))
plt.tight_layout()
plt.savefig('/dbfs/FileStore/row_spatial.png', dpi=300, bbox_inches='tight')
plt.show()
print('✓ Spatial map saved')
```
