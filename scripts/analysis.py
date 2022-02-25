#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axis import Axis
import matplotlib.ticker as ticker
from scipy.stats import pearsonr
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

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
	plt.savefig("../visu/nb_car_by_origin.png")
	plt.close()

def preprocess_dataset():
	inputs = df_algo.drop("Performance", axis="columns")
	target = df_algo["Performance"]
	le_name = LabelEncoder()
	le_origin = LabelEncoder()
	inputs['name_n'] = le_name.fit_transform(inputs["Car"])
	inputs['origin_n'] = le_origin.fit_transform(inputs["Origin"])
	inputs_n = inputs.drop(["Car", "Origin"], axis="columns")
	le_name_1 = LabelEncoder()
	le_origin_1 = LabelEncoder()
	df['name_n'] = le_name_1.fit_transform(df["Car"])
	df['origin_n'] = le_origin_1.fit_transform(df["Origin"])
	total_inputs_n = df.drop(["Car", "Origin"], axis="columns")
	return total_inputs_n, inputs_n, target
    
# Détection des valeurs abérantes (voitures les plus lentes/les moins efficaces)
def potential_outliers():
	model = tree.DecisionTreeClassifier()
	total_inputs_n, inputs_n, target = preprocess_dataset()
	model.fit(inputs_n, target)
	test = model.predict(total_inputs_n)
	bad_vehicule = []
	good_vehicle = []
	for it in range(len(df)):
		if (test[it] == 0):
			bad_vehicule.append(df.iloc[it])
		else:
			good_vehicle.append(df.iloc[it])
	df_good = pd.concat(good_vehicle)
	df_bad= pd.concat(bad_vehicule)
	plt.scatter(df_bad["Acceleration"], df_bad["Displacement"], c="Red")
	plt.scatter(df_good["Acceleration"], df_good["Displacement"], c="DarkBlue")
	plt.savefig("../visu/decistion_tree.png")
	return

# Calcul de corrélation (coefficient de Pearson) entre la puissance du moteur et son nombre de cylindres
def corr_horsepower_cylinder():
	matrix = None

	for it in range(len(df)):
		row = np.array((float(df["Cylinders"][it]), float(df["Horsepower"][it])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	return corr

# Calcul de corrélation (coefficient de Pearson) entre la puissance du moteur et le poids de la voiture
def corr_horsepower_weight():
	matrix = None

	for it in range(len(df)):
		row = np.array((float(df["Weight"][it]), float(df["Horsepower"][it])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	return corr

# Calcul de corrélation (coefficient de Pearson) entre la puissance du moteur et sa cylindrée
def corr_horseower_displacement():
	matrix = None

	for it in range(len(df)):
		row = np.array((float(df["Displacement"][it]), float(df["Horsepower"][it])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	return corr

## Fonction qui regroupe les différents coefficients sur un graphique
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
	plt.savefig("../visu/correlation.png")
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


## Calcul du poids moyen d'une voiture par région
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
	plt.savefig("../visu/Average_car_weight_by_country_of_production.png")
	plt.close()

## Calcul de la puissance moyenne d'une voiture par région
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
	plt.savefig("../visu/Average_car_horse_power_by_country_of_production.png")
	plt.close()


df = pd.read_csv("../datasets/cars.csv", delimiter=",")
df_algo = pd.read_csv("../datasets/cars_algo.csv", delimiter=",")
cars_production_by_country()
corr_graphic(corr_horsepower_cylinder(), corr_horsepower_weight(), corr_horseower_displacement())
average_horse_power_by_country()
average_car_weight_by_country()
potential_outliers()