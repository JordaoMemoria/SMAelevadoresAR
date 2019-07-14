from PoissonGenerator import PoissonGenerator
from FloorsModel import FloorsModel
import matplotlib.pyplot as plt

Ys = []
segs = 3600
lamb = 0.5
elevators = 2
floors = 6
pg = PoissonGenerator(lamb, segs)
env = FloorsModel(elevators, floors, pg, segs/10)

i = 0

while i < 3600 or len(env.peopleSimulator.people) > 0 or len(env.schedule.agents[0].peopleInside) > 0 or len(env.schedule.agents[1].peopleInside) > 0:
    #print("t =",i)
    env.step()
    #print("--------------------------")
    i += 1

nGroup = int(segs*lamb/10)
chunks = [env.timePeople[x:x+nGroup] for x in range(0,len(env.timePeople),nGroup)]

Y = []
for c in chunks:
    Y.append(sum(c)/len(c))

X = []
for x in range(len(Y)):
    X.append(x+1)

# R = []
# for c in chunksRight:
#     R.append(sum(c))
#
# W = []
# for c in chunksRight:
#     W.append(sum(c)/len(c))



print(env.rightChoices)
print(env.wrongChoices)
print(Y)

print(env.schedule.agents[0].w0,env.schedule.agents[0].w1)
print(env.schedule.agents[1].w0,env.schedule.agents[1].w1)


print(sum(env.timePeople)/len(env.timePeople))


#print(R)
#print(W)

plt.plot(X,Y, label='TMS')
#plt.plot([1,2,3,4,5,6,7,8,9,10],env.rightChoices, label='Right')
#plt.plot([1,2,3,4,5,6,7,8,9,10],env.wrongChoices, label='Wrong')
leg = plt.legend(loc='best')
leg.get_frame().set_alpha(0.5)

plt.ylim((0,max(Y)+10))


plt.show()
