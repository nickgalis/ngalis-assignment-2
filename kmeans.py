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
        # Farthest First Traversal initialization
        centroids = []
        centroids.append(data[np.random.randint(0, data.shape[0])])

        for _ in range(1, k):
            distances = np.array([min([np.linalg.norm(x - c) ** 2 for c in centroids]) for x in data])
            next_index = np.argmax(distances)
            centroids.append(data[next_index])

        return np.array(centroids)
    elif method == 'kmeans++':
        # KMeans++ initialization
        centroids = []
        centroids.append(data[np.random.randint(0, data.shape[0])])

        for _ in range(1, k):
            distances = np.array([min([np.linalg.norm(x - c) ** 2 for c in centroids]) for x in data])
            probabilities = distances / distances.sum()
            cumulative_probabilities = probabilities.cumsum()
            r = np.random.rand()

            for j, p in enumerate(cumulative_probabilities):
                if r < p:
                    centroids.append(data[j])
                    break

        return np.array(centroids)
    else:
        raise ValueError("Unknown method")


