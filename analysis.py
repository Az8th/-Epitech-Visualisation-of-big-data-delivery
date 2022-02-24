#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axis import Axis
import matplotlib.ticker as ticker
from scipy.stats import pearsonr


df = pd.read_csv("cars.csv", delimiter=",")

def column(matrix, i):
    return [row[i] for row in matrix]

# Tableau du nombre de voitures produites par région
def cars_production_by_country():
	list_of_country = []
	dict_country = {}
	colors = ['darkcyan', 'lightgreen', 'lightsteelblue']
	for it in range(len(df)):
		if not (df["Origin"][it] in list_of_country):
			list_of_country.append(df["Origin"][it])
		dict_country[df["Origin"][it]] = dict_country.get(df["Origin"][it], 0) + 1
	plt.pie(dict_country.values(), labels=dict_country.keys(), autopct='%1.1f%%')
	plt.title("Comparative of the number of produced cars in different regions")
	plt.savefig("nb_car_by_origin.png")
	plt.close()

def potential_outliers():
	m, b = np.polyfit(df["Acceleration"], df["Displacement"], 1)
	outliers = []
	others = []
	for it in range(len(df)):
		if (df["Displacement"][it] > m * df["Acceleration"][it] + b):
			outliers.append(df.loc[df['Displacement'] == df["Displacement"][it]])
		else:
			others.append(df.loc[df['Displacement'] == df["Displacement"][it]])
	final_outliers = pd.concat(outliers)
	final_others = pd.concat(others)
	plt.plot(df["Acceleration"], m*df["Acceleration"] + b)
	ax = plt.gca()
	final_others.plot.scatter(x="Acceleration", y="Displacement", c="DarkBlue", ax=ax)
	final_outliers.plot.scatter(x="Acceleration", y="Displacement", c="Red", ax=ax)
	plt.savefig("Displacement_vs_Acceleration.png")


def corr_horsepower_cylinder():
	matrix = None

	for it in range(len(df)):
		row = np.array((float(df["Cylinders"][it]), float(df["Horsepower"][it])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	return corr

def corr_horsepower_weight():
	matrix = None

	for it in range(len(df)):
		row = np.array((float(df["Weight"][it]), float(df["Horsepower"][it])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	return corr

#La cylindrée (displacement en anglais) est le volume balayé par le déplacement d'une pièce mobile dans une chambre hermétiquement close pour un mouvement unitaire. 
def corr_horseower_displacement():
	matrix = None

	for it in range(len(df)):
		row = np.array((float(df["Displacement"][it]), float(df["Horsepower"][it])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	return corr

def corr_graphic(corr1, corr2, corr3):
	dict_correlations = dict()
	dict_correlations["Cylinder/Horsepower"] = corr1
	dict_correlations["Weight/Horsepower"] = corr2
	dict_correlations["Displacement/Horsepower"] = corr3
	plt.bar(dict_correlations.keys(), dict_correlations.values())
	ax = plt.gca()
	ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
	plt.ylabel("Pearson's coefficient")
	plt.xlabel("Correlations")
	plt.savefig("correlation.png")
	plt.close()


def np_unknown_cat(acc, arr):
	arrE = np.expand_dims(arr, axis=0)
	if acc is None:
		return arrE
	else:
		return np.concatenate((acc, arrE))

class average:
		def __init__(self):
			self.sum_cal = 0.0
			self.nb = 0.0
		def increment(self, value):
			self.nb += 1
			self.sum_cal += value
		def g_av(self):
			return (self.sum_cal/self.nb)

def average_car_weight_by_country():
	av_us_w = average()
	av_eu_w = average()
	av_jap_w = average()

	for it in range(len(df)):
		if (df["Origin"][it] == "US"): 
			av_us_w.increment(float(df["Weight"][it]))
		if (df["Origin"][it] == "Europe"):
			av_eu_w.increment(float(df["Weight"][it]))
		if (df["Origin"][it] == "Japan"):
			av_jap_w.increment(float(df["Weight"][it]))
	dict_car_weight_by_country = dict()
	dict_car_weight_by_country["US"] = av_us_w.g_av()
	dict_car_weight_by_country["Europe"] = av_eu_w.g_av()
	dict_car_weight_by_country["Japon"] = av_jap_w.g_av()
	plt.bar(dict_car_weight_by_country.keys(), dict_car_weight_by_country.values())
	plt.ylabel("Average car weight")
	plt.xlabel("Region of production")
	plt.savefig("Average_car_weight_by_country_of_production.png")
	plt.close()

def average_horse_power_by_country():
	av_us_hp = average()
	av_eu_hp = average()
	av_jap_hp = average()

	for it in range(len(df)):
		if (df["Origin"][it] == "US"): 
			av_us_hp.increment(float(df["Horsepower"][it]))
		if (df["Origin"][it] == "Europe"):
			av_eu_hp.increment(float(df["Horsepower"][it]))
		if (df["Origin"][it] == "Japan"):
			av_jap_hp.increment(float(df["Horsepower"][it]))
	dict_horsepower_by_country = dict()
	dict_horsepower_by_country["US"] = av_us_hp.g_av()
	dict_horsepower_by_country["Europe"] = av_eu_hp.g_av()
	dict_horsepower_by_country["Japon"] = av_jap_hp.g_av()
	plt.ylabel("Horse power Average")
	plt.xlabel("Region of production")
	plt.bar(dict_horsepower_by_country.keys(), dict_horsepower_by_country.values())
	plt.savefig("Average_car_horse_power_by_country_of_production.png")
	plt.close()

cars_production_by_country()
corr_graphic(corr_horsepower_cylinder(), corr_horsepower_weight(), corr_horseower_displacement())
average_horse_power_by_country()
average_car_weight_by_country()
potential_outliers()