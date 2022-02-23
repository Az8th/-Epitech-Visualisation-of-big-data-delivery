#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


#Car;MPG;Cylinders;Displacement;Horsepower;Weight;Acceleration;Model;Origin
data = pd.read_csv("cars.csv", delimiter=",")
num_arr = np.array(data)
num_arr = np.delete(num_arr, (0), axis=0)

# Tableau du nombre de voitures produites par région
def cars_production_by_country():
	list_of_country = []
	dict_country = {}
	colors = ['darkcyan', 'lightgreen', 'lightsteelblue']
	for it in range(len(num_arr)):
		if not (num_arr[it][8] in list_of_country):
			list_of_country.append(num_arr[it][8])
		dict_country[num_arr[it][8]] = dict_country.get(num_arr[it][8], 0) + 1
		
	print(dict_country)
	plt.pie(dict_country.values(), labels=dict_country.keys(), autopct='%1.1f%%')
	plt.title("Comparatif du nombre de voitures produites en fonction de la région")
	plt.savefig("nb_car_by_origin.png")


def corr_horsepower_cylinder():
	matrix = None

	for it in range(len(num_arr)):
		row = np.array((float(num_arr[it][2]), float(num_arr[it][4])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	print("Corrélation entre le nombre de cylindres d'une voiture et sa puissance en chevaux: %.2f" % corr)

def corr_horsepower_weight():
	matrix = None

	for it in range(len(num_arr)):
		row = np.array((float(num_arr[it][5]), float(num_arr[it][4])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	print("Corrélation entre le poids d'une voiture et sa puissance en chevaux: %.2f" % corr)

#La cylindrée (displacement en anglais) est le volume balayé par le déplacement d'une pièce mobile dans une chambre hermétiquement close pour un mouvement unitaire. 
def corr_horseower_displacement():
	matrix = None

	for it in range(len(num_arr)):
		row = np.array((float(num_arr[it][3]), float(num_arr[it][4])))
		matrix = np_unknown_cat(matrix, row)
	corr = pearsonr(matrix[:, 0], matrix[:, 1])
	corr = round(corr[0], 2)
	print("Corrélation entre la cylindrée d'une voiture et sa puissance en chevaux: %.2f" % corr)

def np_unknown_cat(acc, arr):
	arrE = np.expand_dims(arr, axis=0)
	if acc is None:
		return arrE
	else:
		return np.concatenate((acc, arrE))

def average_car_weight_by_country():
	class average:
		def __init__(self):
			self.sum_weight = 0.0
			self.nb = 0.0
		def increment(self, value):
			self.nb += 1
			self.sum_weight += value
		def g_av(self):
			return (self.sum_weight/self.nb)
	
	av_us_w = average()
	av_eu_w = average()
	av_jap_w = average()

	for it in range(len(num_arr)):
		if (num_arr[it][8] == "US"): 
			av_us_w.increment(float(num_arr[it][5]))
		if (num_arr[it][8] == "Europe"):
			av_eu_w.increment(float(num_arr[it][5]))
		if (num_arr[it][8] == "Japan"):
			av_jap_w.increment(float(num_arr[it][5]))
	
	print("Us-Average_Weight: %.2f, Eu-Average_Weight: %.2f, Jap-Average_Weight: %.2f" % (av_us_w.g_av(), av_eu_w.g_av(), av_jap_w.g_av()))

def average_horse_power_by_country():
	class average:
		def __init__(self):
			self.sum_hp = 0.0
			self.nb = 0.0
		def increment(self, value):
			self.nb += 1
			self.sum_hp += value
		def g_av(self):
			return (self.sum_hp/self.nb)
	
	av_us_hp = average()
	av_eu_hp = average()
	av_jap_hp = average()

	for it in range(len(num_arr)):
		if (num_arr[it][8] == "US"): 
			av_us_hp.increment(float(num_arr[it][4]))
		if (num_arr[it][8] == "Europe"):
			av_eu_hp.increment(float(num_arr[it][4]))
		if (num_arr[it][8] == "Japan"):
			av_jap_hp.increment(float(num_arr[it][4]))
	
	print("Us-Average_Horsep: %.2f, Eu-Average_Horsep: %.2f, Jap-Average_Horsep: %.2f" % (av_us_hp.g_av(), av_eu_hp.g_av(), av_jap_hp.g_av()))

cars_production_by_country()
corr_horsepower_cylinder()
corr_horsepower_weight()
corr_horseower_displacement()
average_horse_power_by_country()
average_car_weight_by_country()