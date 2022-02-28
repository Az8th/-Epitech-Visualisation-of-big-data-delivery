#!/usr/bin/env python3
import pandas as psd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from optparse import OptionParser

#Options parsing
parser = OptionParser()
parser.add_option("-o", "--output", dest="filename", metavar="FILE", default="../visu/visu_cluster.png", help="write result to FILE")
parser.add_option("-c", "--clusters", action="store", type="int", dest="clusters", default=3, help="number of CLUSTERS needed")
parser.add_option("-s", "--show", action="store_true", dest="show", default=False, help="show the result rather than saving it to FILE")
(options, args) = parser.parse_args()

#Parse Dataset
df = pd.read_csv("../datasets/cars.csv", delimiter=",")
df = df.drop(["Car", "MPG", "Cylinders", "Acceleration", "Model", "Origin"], axis="columns")

#Clustering with Kmeans algorithm (kmeans++ avoids bad initialization of centroids)
kmeans = KMeans(n_clusters=options.clusters, init='k-means++').fit(df)
centroids = kmeans.cluster_centers_

#Graph generation
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(df['Displacement'], df['Horsepower'], df['Weight'], c = kmeans.labels_.astype(float), s=10, alpha=0.5)
ax.scatter3D(centroids[:, 0], centroids[:, 1], centroids[:, 2], c='red', s=50)
ax.set_xlabel('Displacement')
ax.set_ylabel('Horsepower')
ax.set_zlabel('Weight')
ax.set_title("Displacement vs Horsepower vs Weight")
if options.show:
    plt.show()
else:
    fig.savefig(options.filename)
