from FloorsModel import FloorsModel
from PoissonGenerator import PoissonGenerator
from PeopleSimulator import ControllerAgent
from Person import Person
import matplotlib.pyplot as plt

Ys = []
segs = 1800
lamb = 0.2
elevators = 3
floors = 6
pg = PoissonGenerator(lamb, segs)
for i in range(30):
    env = FloorsModel(elevators,floors,pg)
    i = 0
    while(
        len(env.schedule.agents[-1].people) > 0 or
        i < segs or
        len(env.schedule.agents[0].peopleToLeave) > 0 or
        len(env.schedule.agents[1].peopleToLeave) > 0 or
        len(env.schedule.agents[2].peopleToLeave) > 0
    ):
    #while(i < 1000):
        #print("t =",i)
        env.step()
        #print("------")
        i += 1

    # print(env.schedule.agents[0].kb.Q)
    # print(env.schedule.agents[0].kb.Nsa)
    # print(env.timePeople)
    # print(len(env.timePeople))
    nGroup = int(segs*lamb/10)
    chunks = [env.timePeople[x:x+nGroup] for x in range(0,len(env.timePeople),nGroup)]
    Y = []
    for c in chunks:
        Y.append(sum(c)/len(c))
    print(Y)
    Ys.append(Y)
    pg.reset()
finalY = []
print(len(Ys))
for i in Ys:
    print(len(i))

for i in range(len(Ys[0])):
    sumI = 0
    for j in range(len(Ys)):
        sumI += Ys[j][i]
    finalY.append(sumI/len(Ys))
X = []
for x in range(len(finalY)):
    X.append(x+1)
print(Y)
plt.plot(X,finalY)
plt.ylim((0,max(finalY)+10))
plt.xlabel("Amostragem agrupada por "+str(nGroup)+" pessoas")
plt.ylabel("Tempo médio em segundos")
plt.show()



# for index, row in env.schedule.agents[0].kb.Q.iterrows():
#     action = None
#     value = None
#     for i in range(len(row)):
#         if value == None:
#             value = row[i]
#             action = row.index[i]
#         elif row[i] > value:
#             value = row[i]
#             action = row.index[i]
#     print(index, action)




# p1 = Person(0,5)
# p2 = Person(0,4)
# p3 = Person(0,3)
# p4 = Person(0,2)
# p5 = Person(0,1)
# p6 = Person(0,1)
# #env.schedule.agents[0].peopleToPickUp = [p1,p2]
#
# for s in env.realStates:
#     for a in env.ACTIONS:
#         print(str(s),a,end=' -> ')
#         env.schedule.agents[0].s = s
#         sl, rl = env.getPerception(s,a,env.schedule.agents[0])
#         print(str(sl),rl)
#         print(env.schedule.agents[0].showAllPeople())
#         print("")