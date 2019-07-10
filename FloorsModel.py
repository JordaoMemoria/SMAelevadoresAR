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
        self.accumulatedRewardOfAgents = []

        p_elevators = []
        for i in range(self.nElevators):
            self.accumulatedRewardOfAgents.append(0)
            a = ElevatorAgent(i, self)
            self.schedule.add(a)
            y = self.random.randrange(self.grid.height)
            p_elevators.append(y)
            self.grid.place_agent(a, (0, y))
        self.currentState = State(p_elevators, nFloors)

        self.peopleSimulator = PeopleSimulator(len(self.schedule.agents), self, pg, self.schedule.agents)
        self.schedule.add(self.peopleSimulator)
        self.moveSecond = True

    def step(self):
        self.schedule.step()
        if self.moveSecond:
            self.moveSecond = False
            print("Elevators acting")
            self.updateState()
        else:
            self.moveSecond = True
        print(self.schedule.agents[0].doorsOpened)
        print(self.currentState)
        self.peopleSimulator.showPeople()
        self.schedule.agents[0].showPeople()
        self.schedule.agents[1].showPeople()

    def updateState(self):
        for i in range(len(self.schedule.agents)-1):
            a = self.schedule.agents[i]
            if a.doorsOpened:
                self.takeOrLeave(a)
            else:
                self.move(a)

    def takeOrLeave(self, agent):
        currentPosition = self.currentState.positions[agent.unique_id]
        if self.currentState.GO[currentPosition][agent.unique_id] == 1:
            self.currentState.GO[currentPosition][agent.unique_id] = 0
            movedPeople = self.peopleSimulator.getPeopleByFloor(currentPosition)
            if len(movedPeople) == 0:
                self.accumulatedRewardOfAgents[agent.unique_id] += -1
                print("----------------------------------------->>>>>>>>>>>>     Agente", agent.unique_id, "foi punido com",-1)

            agent.peopleInside.extend(movedPeople)
            for p in movedPeople:
                self.currentState.LEAVE[p.goTo][agent.unique_id] = 1
                agent.floorsToGo.append(p.goTo)
            agent.floorsToGo = list(dict.fromkeys(agent.floorsToGo))

            if currentPosition == 0:
                self.currentState.buttons[0] = 0
            else:
                self.currentState.buttons[2*currentPosition-1] = 0
                if currentPosition != self.nFloors-1:
                    self.currentState.buttons[2*currentPosition] = 0

        if self.currentState.LEAVE[currentPosition][agent.unique_id] == 1:
            self.currentState.LEAVE[currentPosition][agent.unique_id] = 0
            peopleToGo = self.getPeopleByGoTo(agent,currentPosition)
            for p in peopleToGo:
                r = p.getReward()
                self.accumulatedRewardOfAgents[agent.unique_id] += r
                print("----------------------------------------->>>>>>>>>>>>     Agente", agent.unique_id, "foi recompensado com",r)
            self.saveTimeByPeople(peopleToGo)

        agent.doorsOpened = False

    def move(self, agent):
        if len(agent.floorsToGo) > 0:
            currentPosition = self.currentState.positions[agent.unique_id]
            go = agent.floorsToGo[0]

            if currentPosition in agent.floorsToGo:
                self.currentState.senses[agent.unique_id] = 0
                agent.doorsOpened = True
                agent.floorsToGo.remove(currentPosition)
            elif currentPosition > go:
                self.currentState.positions[agent.unique_id] -= 1
                self.currentState.senses[agent.unique_id] = -1
            elif currentPosition < go:
                self.currentState.positions[agent.unique_id] += 1
                self.currentState.senses[agent.unique_id] = 1
            else:
                print("Some error happended")
        else:
            self.currentState.senses[agent.unique_id] = 0

    def getPerception(self, agent_id):
        r = self.accumulatedRewardOfAgents[agent_id]
        self.accumulatedRewardOfAgents[agent_id] = 0
        return self.currentState, r

    def newAction(self,a,agent,button):
        if a == 'Go':
            self.currentState.GO[int((button+1)/2)][agent.unique_id] = 1
            agent.floorsToGo.append(int((button+1)/2))
            agent.floorsToGo = list(dict.fromkeys(agent.floorsToGo))

    def getPeopleByGoTo(self,agent,goTo):
        peopleByGoTo = []
        for p in agent.peopleInside:
            if p.goTo == goTo:
                peopleByGoTo.append(p)
        agent.peopleInside = [p for p in agent.peopleInside if p not in peopleByGoTo]
        return peopleByGoTo

    def saveTimeByPeople(self,people):
        for p in people:
            self.timePeople.append(p.t)