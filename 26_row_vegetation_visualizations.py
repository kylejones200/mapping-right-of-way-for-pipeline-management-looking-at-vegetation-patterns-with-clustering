import signalplot

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

"""
Blog 26: ROW Vegetation Clustering - Visualization Generator
Generates dendrogram and spatial visualizations for ROW monitoring
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering



np.random.seed(9)
logger.info("Blog 26: ROW Vegetation Clustering - Visualizations")


# ============================================================================
# Generate Synthetic ROW Tile Data
# ============================================================================
logger.info("\nGenerating synthetic ROW tile data...")

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

# Create realistic cluster patterns
# Cluster 0: Dense vegetation
forest_idx = np.random.choice(N_tiles, size=42, replace=False)
df_row.loc[forest_idx, 'ndvi_mean'] = np.random.uniform(0.65, 0.80, 42)
df_row.loc[forest_idx, 'ndvi_std'] = np.random.uniform(0.10, 0.20, 42)
df_row.loc[forest_idx, 'bare_soil_fraction'] = np.random.uniform(0.0, 0.10, 42)
df_row.loc[forest_idx, 'thermal_anomaly_score'] = np.random.normal(-0.02, 0.1, 42)

# Cluster 1: Bare/disturbed
remaining = [i for i in range(N_tiles) if i not in forest_idx]
bare_idx = np.random.choice(remaining, size=28, replace=False)
df_row.loc[bare_idx, 'ndvi_mean'] = np.random.uniform(0.10, 0.25, 28)
df_row.loc[bare_idx, 'bare_soil_fraction'] = np.random.uniform(0.60, 0.85, 28)
df_row.loc[bare_idx, 'thermal_anomaly_score'] = np.random.uniform(0.40, 0.70, 28)

# Cluster 4: Thermal anomaly + exposed soil (smaller, high-risk cluster)
remaining = [i for i in remaining if i not in bare_idx]
thermal_idx = np.random.choice(remaining, size=15, replace=False)
df_row.loc[thermal_idx, 'ndvi_mean'] = np.random.uniform(0.25, 0.40, 15)
df_row.loc[thermal_idx, 'bare_soil_fraction'] = np.random.uniform(0.50, 0.70, 15)
df_row.loc[thermal_idx, 'thermal_anomaly_score'] = np.random.uniform(0.35, 0.55, 15)

logger.info(f"✓ Generated {len(df_row)} tiles")

# ============================================================================
# Visualization 1: Dendrogram
# ============================================================================
logger.info("\nGenerating ROW vegetation dendrogram...")

signalplot.apply(font_family='serif')

features = ['ndvi_mean', 'ndvi_std', 'texture_glcm', 
            'thermal_anomaly_score', 'bare_soil_fraction']
X = df_row[features].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

Z = linkage(X_scaled, method='ward')

fig, ax = plt.subplots(figsize=(12, 5))

dendrogram(Z, ax=ax, truncate_mode='level', p=6, 
           color_threshold=4,
           above_threshold_color="#2b2b2b", 
           no_labels=True,
           link_color_func=lambda k: "#2b2b2b")

ax.set_xlabel('Tile Index (sorted by similarity)')
ax.set_ylabel('Linkage Distance')
ax.set_title('ROW Environmental Clusters Dendrogram', pad=15)

signalplot.tidy_axes(ax)

plt.tight_layout()
signalplot.save('26_row_vegetation_dendrogram.png')
plt.close()
logger.info("✓ Dendrogram saved")

# ============================================================================
# Visualization 2: Cluster Spatial Distribution
# ============================================================================
logger.info("Generating cluster spatial distribution map...")

n_clusters = 5
clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
df_row['cluster_id'] = clustering.fit_predict(X_scaled)

# Use grayscale with different markers and sizes to distinguish clusters
markers = ['o', 's', '^', 'D', 'v']
sizes = [50, 60, 55, 45, 52]
alphas = [0.9, 0.75, 0.85, 0.7, 0.8]
names = ['Dense Veg', 'Bare/Disturbed', 'Mixed Cover', 'Healthy', 'Thermal Anomaly']

fig, ax = plt.subplots(figsize=(12, 4))

for i in range(n_clusters):
    cluster_data = df_row[df_row['cluster_id'] == i]
    # Use shades of gray for different clusters
    gray_value = 0.2 + (i * 0.15)
    ax.scatter(cluster_data['chainage_km'], cluster_data['ndvi_mean'],
               c=str(gray_value), label=f'C{i}: {names[i]}',
               marker=markers[i], s=sizes[i], alpha=alphas[i], 
               edgecolors="#2b2b2b", linewidth=0.8)

ax.set_xlabel('Chainage (km)')
ax.set_ylabel('NDVI (0-1)')
ax.set_title('ROW Vegetation Clusters by Location', pad=15)
ax.legend(loc='upper left', frameon=False, ncol=5)

# Add threshold line (use accent color to call out critical value)
ax.axhline(y=0.7, color="#2980b9", linestyle='--', linewidth=1.5, 
           alpha=0.7, label='NDVI threshold')

signalplot.tidy_axes(ax)

plt.tight_layout()
signalplot.save('26_row_clusters_spatial.png')
plt.close()
logger.info("✓ Spatial distribution map saved")

# ============================================================================
# Visualization 3: Cluster Profiles (Feature Comparison)
# ============================================================================
logger.info("Generating cluster profile comparison...")

cluster_profiles = df_row.groupby('cluster_id')[features].mean()

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Plot 1: NDVI mean by cluster
ax1 = axes[0]
bars1 = ax1.bar(range(n_clusters), cluster_profiles['ndvi_mean'], 
                color="#ffffff", edgecolor="#2b2b2b", 
                linewidth=1.5, alpha=0.9)
ax1.set_ylabel('NDVI Mean')
ax1.set_title('Vegetation Density', pad=15)
ax1.set_xticks(range(n_clusters))
ax1.set_xticklabels([f'C{i}' for i in range(n_clusters)])
signalplot.tidy_axes(ax1)

# Plot 2: Bare soil fraction by cluster
ax2 = axes[1]
bars2 = ax2.bar(range(n_clusters), cluster_profiles['bare_soil_fraction'], 
                color="#ffffff", edgecolor="#2b2b2b", 
                linewidth=1.5, alpha=0.9)
ax2.set_ylabel('Bare Soil Fraction')
ax2.set_title('Soil Exposure', pad=15)
ax2.set_xticks(range(n_clusters))
ax2.set_xticklabels([f'C{i}' for i in range(n_clusters)])
signalplot.tidy_axes(ax2)

# Plot 3: Thermal anomaly score by cluster
ax3 = axes[2]
bars3 = ax3.bar(range(n_clusters), cluster_profiles['thermal_anomaly_score'], 
                color="#ffffff", edgecolor="#2b2b2b", 
                linewidth=1.5, alpha=0.9)
ax3.set_ylabel('Thermal Anomaly Score')
ax3.set_title('Thermal Signature', pad=15)
ax3.set_xticks(range(n_clusters))
ax3.set_xticklabels([f'C{i}' for i in range(n_clusters)])
signalplot.tidy_axes(ax3)

plt.tight_layout()
signalplot.save('26_row_cluster_profiles.png')
plt.close()
logger.info("✓ Cluster profiles saved")

# ============================================================================
# Summary Statistics
# ============================================================================
logger.info("=== All visualizations generated successfully! ===")
logger.info("\nFiles created:")
logger.info("  - 26_row_vegetation_dendrogram.png")
logger.info("  - 26_row_clusters_spatial.png")
logger.info("  - 26_row_cluster_profiles.png")
logger.info("\nCluster Statistics:")
for i in range(n_clusters):
    cluster_data = df_row[df_row['cluster_id'] == i]
    logger.info(f"\n  Cluster {i} ({names[i]}):")
    logger.info(f"    Tiles: {len(cluster_data)}")
    logger.info(f"    Avg NDVI: {cluster_data['ndvi_mean'].mean():.3f}")
    logger.info(f"    Avg Bare Soil: {cluster_data['bare_soil_fraction'].mean():.3f}")
    logger.info(f"    Avg Thermal Anomaly: {cluster_data['thermal_anomaly_score'].mean():.3f}")

logger.info("\nOperational Summary:")
logger.info(f"  High-risk tiles (Clusters 1, 4): {len(df_row[df_row['cluster_id'].isin([1, 4])])}")
logger.info(f"  Standard monitoring (Clusters 0, 2, 3): {len(df_row[~df_row['cluster_id'].isin([1, 4])])}")

