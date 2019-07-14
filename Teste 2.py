import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
from matplotlib import cm
from PoissonGenerator import PoissonGenerator
from FloorsModel import FloorsModel

fig = plt.figure()
ax = plt.axes(projection="3d")

def realFunction(m,n):
    segs = 3600
    lamb = 1

    pg = PoissonGenerator(lamb, segs)
    env = FloorsModel(n, m, pg, segs/10)
    i = 0
    while i < 3600 or len(env.peopleSimulator.people) > 0 or len(env.schedule.agents[0].peopleInside) > 0 or len(env.schedule.agents[1].peopleInside) > 0:
        env.step()
        i += 1
    r = sum(env.timePeople)/len(env.timePeople)

    return r

def z_function2(x,y):
    z = []
    for i in y:
        zl = []
        for j in x:
            print(i,j)
            zl.append(realFunction(i,j))
        z.append(zl)
    return np.asmatrix(z)

x = [2,3,4,5,6,7,8,9,10]
y = [2,8,14,20,26,32,38,44,50]


X, Y = np.meshgrid(x, y)
#Z = z_function2(x, y)

Z = [[37.84960132,35.01018388,37.151507,39.0952381,36.0019396,38.58925144,33.54889768,39.03111111,33.80237154],
     [45.96910431,37.12475742,34.34219269,31.41743247,30.47672508,28.59008126,27.76691317,25.89223897,25.5821727],
     [74.41609636,62.47012061,56.6567332,52.40332871,48.92939245,45.59428571,42.71253482,40.13619667,38.79017985],
     [103.76942426,87.56887686,77.41905565,71.08484848,66.66713444,61.76447552,58.21830209,54.81988636,52.87895501],
     [134.03900325,112.31307757,99.89418736,91.50210379,84.9743228,79.87652315,74.69534556,71.37211917,67.19794843],
     [162.25232019,136.06534707,123.24029058,115.61025927,101.08739255,94.0260223,89.08115778,85.69476906,79.6761932],
     [191.7057842,165.17309813,145.03190572,134.15076072,123.05002779,116.2915493,106.99640288,98.61235294,95.46841512],
     [225.03408773,185.75135281,164.63832266,147.02197802,143.94120864,129.52784919,125.64944248,119.10931289,110.50583215],
     [247.12789078,219.47067039,193.7334814,174.97819487,160.71424589,152.83119366,141.19553546,136.13242134,125.6708613]
     ]


ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, np.asmatrix(Z), rstride=1, cstride=1, cmap=cm.coolwarm, edgecolor='none')

ax.set_zlim(0, 250)
ax.set_xlabel('Número de elevadores')
ax.set_ylabel('Número de andares')
ax.set_zlabel('Tempo médio de serviço')

print(Z)

plt.show()