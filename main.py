from FloorsModel import FloorsModel
from PoissonGenerator import PoissonGenerator
from ControllerAgent import ControllerAgent
from Person import Person

env = FloorsModel(3,6,0.2)
i = 0
while(
        len(env.schedule.agents[-1].people) > 0 or
        i < 86400 or
        len(env.schedule.agents[0].peopleToLeave) > 0 or
        len(env.schedule.agents[1].peopleToLeave) > 0 or
        len(env.schedule.agents[2].peopleToLeave) > 0
):
#while(i < 1000):
    print("t =",i)
    env.step()
    print("------")
    i += 1

print(env.schedule.agents[0].kb.Q)
print(env.schedule.agents[0].kb.Nsa)

for index, row in env.schedule.agents[0].kb.Q.iterrows():
    action = None
    value = None
    for i in range(len(row)):
        if value == None:
            value = row[i]
            action = row.index[i]
        elif row[i] > value:
            value = row[i]
            action = row.index[i]
    print(index, action)




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