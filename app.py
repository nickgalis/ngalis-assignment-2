from flask import Flask, render_template, jsonify, request
import numpy as np
from kmeans import KMeans, initialize_centroids

app = Flask(__name__)

data = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_data', methods=['POST'])
def generate_data():
    global data
    data = np.random.rand(100, 2)  # Generate 100 random 2D data points
    return jsonify(data.tolist())


@app.route('/initialize', methods=['POST'])
def initialize():
    init_method = request.json['method']
    k = request.json['k']
    centroids = initialize_centroids(data, init_method, k)
    return jsonify(centroids.tolist())


@app.route('/step', methods=['POST'])
def step():
    centroids = np.array(request.json['centroids'])
    labels, new_centroids = KMeans.step(data, centroids)
    return jsonify({'labels': labels.tolist(), 'centroids': new_centroids.tolist()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
