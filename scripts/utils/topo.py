from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import umap.umap_ as umap
import matplotlib.pyplot as plt
import numpy as np

def fused_visualization(
    df, values, cmap='jet',
    class_colors=None,
    alpha_overlay=0.6,
    marker_size_overlay=200,
    marker_size_outline=10,
    linewidths_outline=0.9
):
    # Labels and features
    y_raw = df.iloc[:, 0].values       # First column = labels
    X = df.iloc[:, 1:].values           # Rest = features
    
    # Encode classes numerically
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    unique_classes = list(np.unique(y_raw))
    
    # Dimensionality reductions
    X_pca = PCA(n_components=2).fit_transform(X)
    X_tsne = TSNE(n_components=2, perplexity=5, random_state=0).fit_transform(X)
    X_umap = umap.UMAP(random_state=0).fit_transform(X)
    embeddings = [X_pca, X_tsne, X_umap]
    titles = ['PCA', 't-SNE', 'UMAP']

    # Set up subplots
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    for ax, coords, title in zip(axs, embeddings, titles):
        pc1, pc2 = coords[:, 0], coords[:, 1]

        # 1️⃣ Overlay continuous variable as translucent scatter
        sc = ax.scatter(
            pc1, pc2,
            c=values,
            cmap=cmap,
            s=marker_size_overlay,
            alpha=alpha_overlay,
            edgecolor='none'
        )

        # 2️⃣ Outline by class color
        for cls in unique_classes:
            mask = y_raw == cls
            ax.scatter(
                pc1[mask], pc2[mask],
                facecolors='none',
                edgecolor=class_colors.get(cls, 'black') if class_colors else 'black',
                linewidths=linewidths_outline,
                label=cls,
                s=marker_size_outline
            )
        ax.set_title(title)
        ax.set_xlabel('Dim 1')
        ax.set_ylabel('Dim 2')
        ax.grid(True)

    # Single colorbar for continuous variable
    cbar = fig.colorbar(sc, ax=axs, label='Continuous value')
    axs[0].legend(title='Class')
    plt.tight_layout()
    plt.show()






from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
import umap.umap_ as umap


def higher_visualization(df, cmap):
    # Separate labels and features
    y_raw = df.iloc[:, 0].values  # labels (first column)
    X = df.iloc[:, 1:].values     # features (rest columns)

    # Convert string labels to integers
    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    # Prepare figure with 1 row and 3 subplots
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # PCA
    X_pca = PCA(n_components=2).fit_transform(X)
    axs[0].scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap=cmap)
    axs[0].set_title("PCA")

    # t-SNE
    X_tsne = TSNE(n_components=2, perplexity=5, random_state=0).fit_transform(X)
    axs[1].scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap=cmap)
    axs[1].set_title("t-SNE")

    # UMAP
    X_umap = umap.UMAP(random_state=0).fit_transform(X)
    axs[2].scatter(X_umap[:, 0], X_umap[:, 1], c=y, cmap=cmap)
    axs[2].set_title("UMAP")

    plt.tight_layout()
    plt.show()