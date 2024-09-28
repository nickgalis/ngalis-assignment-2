import numpy as np


class KMeans:
    @staticmethod
    def step(data, centroids):
        # Assign each datapoint to the nearest centroid
        distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        # Calculate new centroids from the means of the points
        new_centroids = np.array([data[labels == i].mean(axis=0) for i in range(centroids.shape[0])])

        return labels, new_centroids


def initialize_centroids(data, method, k):
    if method == 'random':
        indices = np.random.choice(data.shape[0], k, replace=False)
        return data[indices]
    elif method == 'farthest':
        # Implement farthest first initialization
        pass
    elif method == 'kmeans++':
        # Implement KMeans++ initialization
        pass
    else:
        raise ValueError("Unknown method")
