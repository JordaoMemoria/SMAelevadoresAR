from mesa import Agent
from random import randint
from Person import Person

class ControllerAgent(Agent):
    def __init__(self, unique_id, model, agents, poisonGenerator):
        super().__init__(unique_id, model)
        self.agents = agents
        self.poissonGenerator = poisonGenerator
        self.peopleWaitingOnFloors = []
        self.people = []

    def getAgents(self):
        return self.agents

    def showPeople(self):
        for p in self.people:
            print(str(p),end=' ')
        print("")

    def step(self):
        print("Controller{")
        print(len(self.people))
        # For the case that people are already waiting busy elevators
        for newP in self.peopleWaitingOnFloors:
            missionToAgent = self.getBestElevatorAgent(newP)
            self.tryToSendMission(missionToAgent, newP)

        # For the case that people just arrived
        nPeopleJustArrive = self.poissonGenerator.get_next_second()
        floorsMission = []
        for i in range(nPeopleJustArrive):
            newP = randint(0,self.model.nFloors-1)
            p = Person(newP,self.sortGoTo(newP))
            self.people.append(p)
            floorsMission.append(newP)
        floorsMission = list(dict.fromkeys(floorsMission))
        # FloorsMisson is for the case that more than one person arrives on the same floor resuting in just one mission
        for newP in floorsMission:
            print("Some person(s) arrives on floor",newP)
            missionToAgent = self.getBestElevatorAgent(newP)
            self.tryToSendMission(missionToAgent, newP)
        print("}")

    def tryToSendMission(self,missionToAgent, floor):
        if missionToAgent != None:
            print("Mission to elevator", missionToAgent.unique_id)
            missionToAgent.s.mission = floor
            peopleByFloor = self.getPeopleByFloor(floor)
            self.people = [n for n in self.people if n not in peopleByFloor]
            missionToAgent.peopleToPickUp = peopleByFloor
            self.updateWaiting()
        else:
            self.peopleWaitingOnFloors.append(floor)
            self.peopleWaitingOnFloors = list(dict.fromkeys(self.peopleWaitingOnFloors))

    def updateWaiting(self):
        newWaiting = []
        for p in self.people:
            newWaiting.append(p.floor)
        self.peopleWaitingOnFloors = list(dict.fromkeys(newWaiting))

    def getBestElevatorAgent(self,floor):
        missionToAgent = None
        dist = None
        for a in self.agents:
            if a.s.mission == self.model.nFloors:
                d = abs(floor - a.s.floor)
                if missionToAgent == None:
                    missionToAgent = a
                    dist = d
                elif d < dist:
                    missionToAgent = a
                    dist = d
        return missionToAgent

    def sortGoTo(self,floor):
        goTo = randint(0,self.model.nFloors-1)
        while floor == goTo:
            goTo = randint(0,self.model.nFloors-1)
        return goTo

    def getPeopleByFloor(self,floor):
        peopleByFloor = []
        for p in self.people:
            if p.floor == floor:
                peopleByFloor.append(p)
        return peopleByFloor