from PoissonGenerator import PoissonGenerator
from FloorsModel import FloorsModel

Ys = []
segs = 1800
lamb = 0.5
elevators = 3
floors = 6
pg = PoissonGenerator(lamb, segs)
env = FloorsModel(elevators,floors,pg)


for i in range(100):
    print("t =",i)
    env.step()
    print("--------------------------")