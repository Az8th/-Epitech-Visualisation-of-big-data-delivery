#!/usr/bin/env python3
from optparse import OptionParser
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

#Options parsing
parser = OptionParser()
parser.add_option("-o", "--output", dest="filename", metavar="FILE", default="artificial_dataset.csv", help="write generated dataset to FILE")
parser.add_option("-l", "--lines", action="store", type="int", dest="lines", default=300, help="number of LINES needed")
(options, args) = parser.parse_args()


#Generate correlations matrix
neg_coef = np.array([[1., -1],[-1, 1.]])
neut_coef = np.array([[1., 0],[0, 1.]])
pos_coef = np.array([[1., 1],[1, 1.]])

# Generate random mean values (except for 2.5 which is mandatory)
rng = np.random.default_rng()
mu = rng.random(5)
mu = np.append(mu, 2.5)

# Generate the random samples according to the given correlation
ds = rng.multivariate_normal(mu[:2], neg_coef, size=options.lines)
ds = np.hstack((ds, rng.multivariate_normal(mu[2:4], neut_coef, size=options.lines)))
ds = np.hstack((ds, rng.multivariate_normal(mu[4:6], pos_coef, size=options.lines)))

# Adding an integer column 
ds = np.column_stack((ds, rng.integers(-2048, 2048,size=options.lines)))

# Saving to file 
np.savetxt(options.filename, ds, delimiter=",")