from PoissonGenerator import PoissonGenerator
from FloorsModel import FloorsModel
import matplotlib.pyplot as plt

Ys = []
segs = 3600
lamb = 0.5
elevators = 4
floors = 16
T1 = [18,11,15,8,8,34,46,40,34,46,9,10,6,6,9]
T2 = [17,17,13,13,10,34,31,26,41,38,13,12,14,8,12]

T3Up = [0,1,2,2,0,2,2,0,2,0,1,2,1,0,0]
T3Down = [7,10,7,9,12,10,8,8,10,18,11,6,12,2,15]


pg = PoissonGenerator()
pg.setUpDownOrder(T3Up, T3Down)


tW = []
tJ = []
tC = []

for j in range(10):
    pg.reset()
    env = FloorsModel(elevators, floors, pg, segs/10)

    i = 0
    while i < 900 or len(env.peopleSimulator.people) > 0 or len(env.schedule.agents[0].peopleInside) > 0 or len(env.schedule.agents[1].peopleInside) > 0 or len(env.schedule.agents[2].peopleInside) > 0 or len(env.schedule.agents[3].peopleInside) > 0:
        #print("t =",i)
        env.step()
        #print("--------------------------")
        i += 1
    i = 0

    print(env.timePeopleWait)
    print(env.timePeopleJourney)
    print(env.timeCrowding)
    tW.append(sum(env.timePeopleWait)/len(env.timePeopleWait))
    tJ.append(sum(env.timePeopleJourney)/len(env.timePeopleJourney))
    tC.append(sum(env.timeCrowding)/len(env.timeCrowding)*100)

print('tW:',sum(tW)/len(tW))
print('tJ:',sum(tJ)/len(tJ))
print('tC:',sum(tC)/len(tC))

