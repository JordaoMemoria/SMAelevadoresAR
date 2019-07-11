import matplotlib.pyplot as plt
import numpy as np

# ax = plt.subplot(111)
# t1 = np.arange(0.0, 1.0, 0.01)
# for n in [1, 2, 3, 4]:
#     plt.plot(t1, t1**n, label="n=%d"%(n,))
#
# leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
# leg.get_frame().set_alpha(0.5)

X = [1,2,3,4,5]
Y = [1,2,3,4,5]
Z = [2,3,4,5,6]
J = [3,4,5,6,7]

plt.plot(X,Y)
plt.plot(X,Z)
plt.plot(X,J)

plt.show()