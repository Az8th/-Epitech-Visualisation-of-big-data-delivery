import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

#Car;MPG;Cylinders;Displacement;Horsepower;Weight;Acceleration;Model;Origin
data = pd.read_csv("cars.csv", delimiter=";")
num_arr = np.array(data)
num_arr = np.delete(num_arr, (0), axis=0)

## Calcule la moyenne d'étoiles de tous les produits
def average_rating():
	average_rating_products = 0.0
	nb_of_nan = 0
	for it in range(len(num_arr)):
		if (math.isnan(float(num_arr[it][6])) is False):
			average_rating_products += float(num_arr[it][6])
		else:
			nb_of_nan += 1
	average_rating_products = average_rating_products / len(num_arr)
	return average_rating_products


def cars_production_by_country():
	list_of_country = []
	dict_country = {}
	for it in range(len(num_arr)):
		if not (num_arr[it][8] in list_of_country):
			list_of_country.append(num_arr[it][8])
		dict_country[num_arr[it][8]] = dict_country.get(num_arr[it][8], 0) + 1
		
	print(dict_country)
	plt.bar(dict_country.keys(), dict_country.values())
	plt.xlabel("Pays")
	plt.ylabel("nb de voitures")
	plt.title("Comparatif du nombre de voitures produites en fonction du pays")
	plt.show()
	plt.savefig("nb_car_by_origin.png")



cars_production_by_country()