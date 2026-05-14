import sys
import os

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# Add parent directory to path to import plot_style
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plot_style import set_tufte_defaults, apply_tufte_style, save_tufte_figure, COLORS

"""
Visualization generation for Blog 15: ROW Encroachment Detection with DINOv2
Creates minimalist-style visualizations for encroachment detection.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import warnings


# Add parent directory to path to import plot_style
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings('ignore')

def apply_minimalist_style_manual(ax):
    """Apply minimalist style components manually to axis."""
    plt.rcParams["font.family"] = "serif"
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_position(("outward", 5))
    ax.spines["bottom"].set_position(("outward", 5))
    ax.grid(False)

def generate_embeddings_with_encroachment(n_images=5000):
    """
    Generate synthetic DINOv2 embeddings with encroachment patterns.
    
    Classes:
    0: Normal ROW (bare ground, grass) - 85%
    1: Vegetation encroachment - 8%
    2: Structure encroachment (buildings, equipment) - 5%
    3: Vehicle/activity - 2%
    """
    np.random.seed(42)
    
    # Class distribution
    n_normal = int(n_images * 0.85)
    n_vegetation = int(n_images * 0.08)
    n_structure = int(n_images * 0.05)
    n_vehicle = n_images - n_normal - n_vegetation - n_structure
    
    embeddings = []
    labels = []
    
    # Normal ROW (tight cluster)
    normal_embeddings = np.random.randn(n_normal, 384) * 0.25
    embeddings.append(normal_embeddings)
    labels.extend([0] * n_normal)
    
    # Vegetation encroachment (separate cluster)
    veg_center = np.ones(384) * 0.6
    veg_embeddings = np.random.randn(n_vegetation, 384) * 0.35 + veg_center
    embeddings.append(veg_embeddings)
    labels.extend([1] * n_vegetation)
    
    # Structure encroachment (outliers)
    struct_center = np.ones(384) * 1.3
    struct_embeddings = np.random.randn(n_structure, 384) * 0.5 + struct_center
    embeddings.append(struct_embeddings)
    labels.extend([2] * n_structure)
    
    # Vehicle/activity (outliers)
    vehicle_center = np.ones(384) * -0.9
    vehicle_embeddings = np.random.randn(n_vehicle, 384) * 0.4 + vehicle_center
    embeddings.append(vehicle_embeddings)
    labels.extend([3] * n_vehicle)
    
    embeddings = np.vstack(embeddings)
    labels = np.array(labels)
    
    return embeddings, labels

def create_main_embedding_space_plot(plot: bool = False):
    """
    Create t-SNE projection showing encroachment detection in embedding space.
    """
    logger.info("Generating main embedding space visualization...")
    
    # Generate embeddings
    embeddings, labels = generate_embeddings_with_encroachment(n_images=5000)
    
    # t-SNE projection
    logger.info("  Running t-SNE dimensionality reduction...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)
    embeddings_2d = tsne.fit_transform(embeddings)
    
    # Create figure
    if plot:
        fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define colors and labels
        colors = {
            0: '#CCCCCC',  # Gray for normal ROW
            1: '#2ECC40',  # Green for vegetation
            2: '#FF4136',  # Red for structures
            3: '#FF851B'   # Orange for vehicles
        }
    
        class_names = {
            0: 'Normal ROW (Baseline)',
            1: 'Vegetation Encroachment',
            2: 'Structure Encroachment',
            3: 'Vehicle/Activity'
        }
    
    # Plot each class
        for class_id in [0, 1, 2, 3]:
            mask = labels == class_id
            ax.scatter(
                embeddings_2d[mask, 0],
                embeddings_2d[mask, 1],
                c=colors[class_id],
                label=class_names[class_id],
                alpha=0.5 if class_id == 0 else 0.8,
                s=15 if class_id == 0 else 40,
                edgecolors='black',
                linewidth=0.5
            )
    
    # Apply minimalist style
        apply_minimalist_style_manual(ax)
    
    # Labels and title
        ax.set_xlabel('t-SNE Dimension 1', fontsize=10)
        ax.set_ylabel('t-SNE Dimension 2', fontsize=10)
        ax.set_title('ROW Encroachment Detection via DINOv2 Embeddings', 
                     fontsize=12, fontweight='bold', loc='left', pad=20)
    
    # Legend
        ax.legend(loc='upper right', frameon=False, fontsize=9)
    
    # Add annotation
        n_encroachment = np.sum(labels > 0)
        ax.text(0.02, 0.02, 
                f'5,000 ROW images | 384-dim DINOv2 embeddings | {n_encroachment} encroachments ({n_encroachment/len(labels)*100:.1f}%)',
                transform=ax.transAxes, fontsize=8, 
                verticalalignment='bottom', color='black')
    
        plt.tight_layout()
        plt.savefig('/Users/k.jones/Desktop/blogs/blog_posts/15_row_encroachment_dinov2_main.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()
    
    logger.info(f"✓ Main embedding space visualization saved")
    logger.info(f"  Total images: {len(labels)}")
    logger.info(f"  Encroachments: {n_encroachment} ({n_encroachment/len(labels)*100:.1f}%)")

def create_temporal_encroachment_trend(plot: bool = False):
    """
    Create time series showing encroachment detection over time.
    """
    logger.info("Generating temporal encroachment trend visualization...")
    
    np.random.seed(42)
    
    # Monthly data for 2 years
    months = np.arange(24)
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] * 2
    
    # Baseline encroachment rate with seasonal pattern
    baseline = 3.0 + 2.0 * np.sin(months * np.pi / 6)  # Summer peaks
    
    # Add growing trend (vegetation growth over time)
    trend = 0.15 * months
    
    # Vegetation encroachment
    vegetation = baseline + trend + np.random.randn(24) * 0.5
    
    # Structure encroachment (sporadic)
    structure = np.zeros(24)
    structure[[5, 6, 12, 18, 19]] = np.random.uniform(1.5, 3.0, 5)
    structure += np.random.randn(24) * 0.2
    structure = np.clip(structure, 0, None)
    
    # Vehicle activity (more variable)
    vehicle = 1.0 + np.random.randn(24) * 0.8
    vehicle = np.clip(vehicle, 0, None)
    
    # Total encroachment
    total = vegetation + structure + vehicle
    
    # Create figure
    if plot:
        fig, ax = plt.subplots(figsize=(12, 6))
    
    # Stacked area plot
        ax.fill_between(months, 0, vehicle, 
                        color='black', alpha=0.7, label='Vehicle/Activity',
                        edgecolor='black', linewidth=0.5)
    
        ax.fill_between(months, vehicle, vehicle + structure,
                        color='black', alpha=0.7, label='Structure Encroachment',
                        edgecolor='black', linewidth=0.5)
    
        ax.fill_between(months, vehicle + structure, total,
                        color='black', alpha=0.7, label='Vegetation Encroachment',
                        edgecolor='black', linewidth=0.5)
    
    # Total line
        ax.plot(months, total, 'k-', linewidth=2, label='Total Encroachment', zorder=5)
    
    # Apply minimalist style
        apply_minimalist_style_manual(ax)
    
        ax.set_xlabel('Month', fontsize=11)
        ax.set_ylabel('Encroachment Rate (% of ROW)', fontsize=11)
        ax.set_title('ROW Encroachment Trends Over Time', 
                     fontsize=13, fontweight='bold', loc='left', pad=20)
    
    # X-axis labels
        ax.set_xticks(months[::2])
        ax.set_xticklabels([f"{month_labels[i]}\n{'2023' if i < 12 else '2024'}" 
                            for i in range(0, 24, 2)], fontsize=9)
    
        ax.legend(loc='upper left', frameon=False, fontsize=9)
    
    # Add annotation for growing trend
        ax.annotate('Growing Vegetation\nEncroachment Trend', 
                   xy=(18, total[18]), xytext=(14, total[18] + 3),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                   fontsize=9, bbox=dict(boxstyle='round', facecolor='white', 
                                        edgecolor='black', linewidth=1))
    
        plt.tight_layout()
        plt.savefig('/Users/k.jones/Desktop/blogs/blog_posts/15_row_encroachment_temporal.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()
    
    logger.info("✓ Temporal encroachment trend visualization saved")

def main():
    """Generate all visualizations for Blog 15."""
    set_tufte_defaults()
    logger.info("Blog 15: ROW Encroachment Detection - Visualizations")
    logger.info()
    
    create_main_embedding_space_plot()
    create_temporal_encroachment_trend()
    
    logger.info()
    logger.info("All visualizations generated successfully!")
    logger.info()
    logger.info("Files created:")
    logger.info("  - 15_row_encroachment_dinov2_main.png")
    logger.info("  - 15_row_encroachment_temporal.png")

if __name__ == "__main__":
    main()

