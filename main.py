from FloorsModel import FloorsModel
from PoissonGenerator import PoissonGenerator
from ControllerAgent import ControllerAgent

env = FloorsModel(3,6,0.2)

for i in range(100):
    print("t =",i)
    env.step()
    print("------")