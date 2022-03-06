#!/usr/bin/env python3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
pd.options.mode.chained_assignment = None

class average:
		def __init__(self):
			self.sum_cal = 0.0
			self.nb = 0.0
		def increment(self, value):
			self.nb += 1
			self.sum_cal += value
		def g_av(self):
			return (self.sum_cal/self.nb)


df = pd.read_csv("data.csv", delimiter=",")

def preprocess_dataset():
	le_origin, le_origin_1 = LabelEncoder(), LabelEncoder()
	df_range = df.iloc[0:150]

	#Traitement du dataset d'entrainement
	df_range['origin_n'] = le_origin.fit_transform(df_range["Origin"])
	inputs_n = df_range.drop(["Car", "Origin", "Weight", "Model", "origin_n", "Cylinders"], axis="columns")

	#Traitement du dataset final
	df['origin_n'] = le_origin_1.fit_transform(df["Origin"])
	total_inputs_n = df.drop(["Car", "Origin", "Weight", "Model", "origin_n", "Cylinders"], axis="columns")

	target = df_range["Weight"]
	total_target = df["Weight"]
	return total_inputs_n, inputs_n, target, total_target

def predict_weight():
	model = LinearRegression()
	total_inputs_n, inputs_n, target, total_target = preprocess_dataset()
	model.fit(inputs_n, target)
	print("Score du modèle sur le dataset complet: %.2f" % model.score(total_inputs_n, total_target))
	test = model.predict(total_inputs_n)
	le_name = LabelEncoder()
	df["name_n"] = le_name.fit_transform(df["Car"])
	test_average, real_average = average(), average()
	for it in range(len(df)):
		test_average.increment(float(test[it]))
		real_average.increment(float(df["Weight"][it]))
	diff = test_average.g_av() - real_average.g_av()
	print("Différence moyenne entre le dataset et le modèle: %.2f Kg" % diff)
	return

predict_weight()