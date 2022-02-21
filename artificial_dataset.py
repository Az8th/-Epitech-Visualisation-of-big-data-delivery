import numpy as np

dataset = np.zeros((50, 6))
print(dataset)

np.savetxt('data.csv', dataset, delimiter=',')