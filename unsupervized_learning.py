#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from optparse import OptionParser
from sys import exit

def eval_score(df, c1, c2):
    score = 0
    for i, row in df.iterrows():
        if (row[c1] == row[c2]):
            score += 1
    return (score * 100 / (i + 1))

def list_parse(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

#Options parsing
parser = OptionParser()
parser.add_option("-o", "--output", dest="filename", metavar="FILE", default="visu_cluster.png", help="write result to FILE")
parser.add_option("-c", "--clusters", action="store", type="int", dest="clusters", default=3, help="number of CLUSTERS needed")
parser.add_option("-s", "--show", action="store_true", dest="show", default=False, help="show the result rather than saving it to FILE")
parser.add_option("-d", "--data", action="callback", type="string", dest="columns", callback=list_parse, default=["Displacement","Horsepower"], help="use the DATA columns for prediction (2 or 3 dimensions only)")
(options, args) = parser.parse_args()

#Parse Dataset
raw_df = pd.read_csv("data.csv", delimiter=",")
if (len(options.columns) not in range(2,4)):
    print("Error: Incorrect amount of dimensions")
    exit(1)
try:
    df = raw_df[options.columns]
except:
    print("Given column not present in dataset")
    exit(1)

#Clustering with Kmeans algorithm (kmeans++ avoids bad initialization of centroids)
kmeans = KMeans(n_clusters=options.clusters, init='k-means++', random_state=0).fit(df)
kmeans.predict(df)
centroids = kmeans.cluster_centers_
raw_df['Cluster'] = kmeans.labels_.astype(int)

#Transform cluster attribution to number of cylinders (2, 4 or 8)
raw_df['Cluster'] = raw_df['Cluster'].apply(lambda x:2 ** (x + 1))

#Graph generation
fig = plt.figure()
if (len(options.columns) == 3):
    ax = plt.axes(projection='3d')
    s = ax.scatter3D(raw_df[options.columns[0]], raw_df[options.columns[1]], raw_df[options.columns[2]], c = raw_df['Cluster'], s=10, alpha=0.5)
    ax.scatter3D(centroids[:, 0], centroids[:, 1], centroids[:, 2], c='red', s=50)
    ax.set_zlabel(options.columns[2])
else:
    ax = plt.axes()
    s = ax.scatter(raw_df[options.columns[0]], raw_df[options.columns[1]], c = raw_df['Cluster'], s=10, alpha=0.5)
    ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
ax.set_xlabel(options.columns[0])
ax.set_ylabel(options.columns[1])
ax.set_title("Number of cylinders prediction")
cb=plt.colorbar(s)
cb.set_label('cylinders')

#Printing
print ("Prediction accuracy: %.2f%%" % eval_score(raw_df, "Cluster", "Cylinders"))

if options.show:
    plt.show()
else:
    fig.savefig(options.filename)
