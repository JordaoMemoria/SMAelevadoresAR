from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from ElevatorAgent import ElevatorAgent
from PeopleSimulator import PeopleSimulator
from State import State


class FloorsModel(Model):

    def __init__(self, nElevators, nFloors, pg, nTime):
        self.nElevators = nElevators
        self.nFloors = nFloors
        self.grid = MultiGrid(1, nFloors, False)
        self.schedule = BaseScheduler(self)

        self.ACTIONS = ['Go', 'Ignore']

        self.timePeople = []
        self.rightChoices = []
        self.wrongChoices = []

        self.rightChoice = 0
        self.wrongChoice = 0
        self.t = 0
        self.nTime = nTime

        p_elevators = []
        for i in range(self.nElevators):
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
        self.t += 1
        if self.t == self.nTime:
            self.rightChoices.append(self.rightChoice)
            self.wrongChoices.append(self.wrongChoice)
            self.rightChoice = 0
            self.wrongChoice = 0
            self.t = 0


        self.schedule.step()
        if self.moveSecond:
            self.moveSecond = False
            #print("Elevators acting")
            self.updateState()
        else:
            self.moveSecond = True

        # print(self.schedule.agents[0].doorsOpened, self.schedule.agents[1].doorsOpened)
        # print("Agent 0", self.schedule.agents[0].floorsToGo)
        # print("Agent 1", self.schedule.agents[1].floorsToGo)
        # print(self.currentState)
        # self.peopleSimulator.showPeople()
        # self.schedule.agents[0].showPeople()
        # self.schedule.agents[1].showPeople()


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
        return self.currentState

    def newAction(self,action, agent, button, state):
        #print(a)
        if action == 'Go':
            self.currentState.GO[int((button+1)/2)][agent.unique_id] = 1
            agent.floorsToGo.append(int((button+1)/2))
            agent.floorsToGo = list(dict.fromkeys(agent.floorsToGo))
            self.peopleSimulator.setPeopleByFloorWithElevators(int((button+1)/2))

        resp = agent.getD(state, button, agent)
        if (resp == 1 and action == 'Go') or (resp == -1 and action == 'Ignore'):
            self.rightChoice += 1
            return 1
        elif (resp == -1 and action == 'Go') or (resp == 1  and action == 'Ignore'):
            self.wrongChoice += 1
            return -1




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