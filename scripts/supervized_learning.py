#!/usr/bin/env python3
import pandas as pd

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

df = pd.read_csv("../datasets/cars.csv", delimiter=",")
