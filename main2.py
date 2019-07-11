from PoissonGenerator import PoissonGenerator
from FloorsModel import FloorsModel
import matplotlib.pyplot as plt

Ys = []
segs = 3600
lamb = 0.1
elevators = 2
floors = 6
pg = PoissonGenerator(lamb, segs)
env = FloorsModel(elevators,floors,pg)

i = 0

while i < 36000 or len(env.peopleSimulator.people) > 0 or len(env.schedule.agents[0].peopleInside) > 0 or len(env.schedule.agents[1].peopleInside) > 0:
    #print("t =",i)
    env.step()
    #print("--------------------------")
    i += 1

nGroup = int(segs*lamb/2)
chunks = [env.timePeople[x:x+nGroup] for x in range(0,len(env.timePeople),nGroup)]
Y = []
for c in chunks:
    Y.append(sum(c)/len(c))
print(Y)
X = []
for x in range(len(Y)):
    X.append(x+1)

plt.plot(X,Y)
plt.ylim((0,max(Y)+10))
plt.xlabel("Amostragem agrupada por "+str(nGroup)+" pessoas")
plt.ylabel("Tempo médio em segundos")
plt.show()
