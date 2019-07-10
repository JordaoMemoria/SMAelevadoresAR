from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from ElevatorAgent import ElevatorAgent
from PeopleSimulator import PeopleSimulator
from State import State


class FloorsModel(Model):
    def __init__(self, nElevators, nFloors, pg):
        self.nElevators = nElevators
        self.nFloors = nFloors
        self.grid = MultiGrid(1, nFloors, False)
        self.schedule = BaseScheduler(self)

        self.ACTIONS = ['Go', 'Ignore']

        self.timePeople = []

        p_elevators = []
        for i in range(self.nElevators):
            a = ElevatorAgent(i, self)
            self.schedule.add(a)
            y = self.random.randrange(self.grid.height)
            p_elevators.append(y)
            self.grid.place_agent(a, (0, y))
        self.currentState = State(p_elevators, nFloors)

        for s in self.schedule.agents:
            s.initLastState()

        self.peopleSimulator = PeopleSimulator(len(self.schedule.agents), self, pg)
        self.schedule.add(self.peopleSimulator)
        self.moveSecond = True

    def step(self):
        print(self.currentState)
        self.schedule.step()
        if self.moveSecond:
            self.moveSecond = False
            self.updateState()
        else:
            self.moveSecond = True

    def updateState(self):
        for i in range(len(self.schedule.agents)-1):
            a = self.schedule.agents[i]

            print(a.unique_id)

    def moveByGoCalls(self, unique_id):
        pass

    def getPerception(self):
        return self.currentState, 0

    def newAction(self,a,agent,button):
        if a == 'Go':
            self.currentState.GO[int((button+1)/2)][agent.unique_id] = 1

    def getPeopleByGoTo(self,agent,goTo):
        peopleByGoTo = []
        for p in agent.peopleToLeave:
            if p.goTo == goTo:
                peopleByGoTo.append(p)
        return peopleByGoTo

    def saveTimeByPeople(self,people):
        for p in people:
            self.timePeople.append(p.t)