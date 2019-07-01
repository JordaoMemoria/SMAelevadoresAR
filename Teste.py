import numpy as np
import matplotlib.pyplot as plt
Y = np.random.poisson(0.5, 86400)
X = []

print(Y)

plt.hist(Y,histtype='stepfilled')
plt.show()
