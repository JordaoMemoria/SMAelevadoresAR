from mesa import Agent
from random import randint
class ControllerAgent(Agent):
    def __init__(self, unique_id, model, agents, poisonGenerator):
        super().__init__(unique_id, model)
        self.agents = agents
        self.poissonGenerator = poisonGenerator

    def getAgents(self):
        return self.agents

    def step(self):
        nPeopleJustArrive = self.poissonGenerator.get_next_second()
        for i in range(nPeopleJustArrive):
            newP = randint(0,self.model.nFloors-1)
            print("Someone arrives on floor",newP)

            missionToAgent = None
            dist = None

            for a in self.agents:
                if a.mission == 0:
                    d = abs(newP-a.pos[1])
                    if missionToAgent == None:
                        missionToAgent = a
                        dist = d
                    elif d < dist:
                        missionToAgent = a
                        dist = d
            print("Mission to elevator",missionToAgent.unique_id)



