#!/usr/bin/env python3
import sys
import getopt
import pandas as pd
import matplotlib.pyplot as plt

features = [
	"Car",
	"MPG",
	"Cylinders",
	"Displacement",
	"Horsepower",
	"Weight",
	"Acceleration",
	"Model",
	"Origin"
]

df = pd.read_csv("data.csv", delimiter=",")
max_range = len(df.index)
min_range = 0
xaxis = 6
yaxis = 3

def visualisation():
	df_range = df.iloc[min_range:max_range]
	plt.bar(df_range[features[xaxis]], df_range[features[yaxis]])
	plt.xlabel(features[xaxis])
	plt.ylabel(features[yaxis])
	plt.title(features[xaxis] + " vs " + features[yaxis])
	plt.savefig("../visu/visu_2.png")

try:
	opts, args = getopt.getopt(sys.argv[1:], "hx:y", ["help","xaxis=", "yaxis=", "min=", "max="])
	for name, value in opts:
		if name in ['-h', '--help']: 
			print("Usage: python3 visualization_1.py --xaxis --yaxis [-h] [--min] [--max]\n\t--xaxis - Absisses features, default value: \"Acceleration\"\n\t--yaxis - Ordinate features, default value: \"Dispacement\"\n\tFeatures list: %s\n\t[--min] - Range min option\n\t[--max] - Range max option\n\t[--help] - Help command" % (str(features)))
		elif name in ['-x', "--xaxis"]:
			xaxis = int(value)
		elif name in ["-y", '--yaxis']:
			yaxis = int(value)
		elif name in ['--min']:
			if int(value) < 0 & int(value) > 406:
				raise Exception("Min out of range")
			min_range = int(value)
		elif name in ['--max']:
			if int(value) < 0 & int(value) > 406:
				raise Exception("Min out of range")
			max_range = int(value)
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)
visualisation()
	
      

