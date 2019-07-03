from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ElevatorAgent import ElevatorAgent
from ControllerAgent import ControllerAgent
from PoissonGenerator import PoissonGenerator
from KnowledgeBase import KnowledgeBase
from ElevatorAgent import State

class FloorsModel(Model):
    def __init__(self, nElevators, nFloors, pg):
        self.nElevators = nElevators
        self.nFloors = nFloors
        self.grid = MultiGrid(1, nFloors, False)
        self.schedule = RandomActivation(self)

        self.STATES,self.realStates = self.createStates()
        self.ACTIONS = ['Up', 'Down', 'Close', 'Open', 'Keep']
        kb = KnowledgeBase(actions=self.ACTIONS, states=self.STATES)

        self.timePeople = []

        for i in range(self.nElevators):
            a = ElevatorAgent(i, self, kb)
            self.schedule.add(a)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (0, y))
        self.schedule.step()
        self.controllerAgent = ControllerAgent(i+1, self, self.schedule.agents, pg)
        self.schedule.add(self.controllerAgent)

    def step(self):
        # This steps represents 1 second
        self.schedule.step()

    def createStates(self):
        states = []
        realStates = []
        for i in range(self.nFloors):
            for j in range(self.nFloors+1):
                for z in range(2):
                    if z == 0:
                        realStates.append(State(i,False,j))
                        states.append(str('('+str(i)+','+str(False)+','+str(j)+')'))
                    else:
                        realStates.append(State(i, True, j))
                        states.append(str('('+str(i)+','+str(True)+','+str(j)+')'))
        return states,realStates

    def getPerception(self, s, a, agent):
        # To start a agent
        if s == None:
            return State(agent.pos[1], False, self.nFloors), 0

        if s.floor == s.mission and s.doorOpened == True:
            agent.peopleToLeave = agent.peopleToPickUp
            agent.peopleToPickUp = []
            newMission = self.getNewMission(agent)
            return State(s.floor, True, newMission), 1
        #To receive or leave people on missions
        elif s.floor == s.mission and s.doorOpened == False and a == 'Open':
            #If picking people
            if len(agent.peopleToPickUp) > 0 and len(agent.peopleToLeave) == 0:
                agent.peopleToLeave = agent.peopleToPickUp
                agent.peopleToPickUp = []
                newMission = self.getNewMission(agent)
                return State(s.floor, True, newMission), 1
            #If leaving people
            elif len(agent.peopleToPickUp) == 0 and len(agent.peopleToLeave) > 0:
                pByFloor = self.getPeopleByGoTo(agent, s.floor)
                self.saveTimeByPeople(pByFloor)
                agent.peopleToLeave = [n for n in agent.peopleToLeave if n not in pByFloor]
                newMission = self.getNewMission(agent)
                if newMission == None:
                    return State(s.floor, True, self.nFloors), 1
                else:
                    return State(s.floor, True, newMission), 1
        #To teach not to move with door opened
        elif s.doorOpened == True and (a == 'Up' or a == 'Down'):
            return State(s.floor, True, s.mission),-1
        #To teach not to crash on ceil and floor
        elif (s.floor == self.nFloors-1 and a == 'Up') or (s.floor == 0 and a == 'Down'):
            return State(s.floor, s.doorOpened, s.mission),-1
        #To reward the agent when it become next to the mission
        elif s.doorOpened == False and a == 'Up' and s.mission != self.nFloors and s.floor < s.mission:
            return State(s.floor+1, False, s.mission), self.getRewardByDist(s.floor+1, s.mission)
        elif s.doorOpened == False and a == 'Down' and s.mission != self.nFloors and s.floor > s.mission:
            return State(s.floor-1, False, s.mission), self.getRewardByDist(s.floor-1, s.mission)
        #To teach the agent to close the door when it has a misson
        elif s.mission != self.nFloors and s.doorOpened == True and a == 'Close':
            return State(s.floor, False, s.mission), self.getRewardByDist(s.floor, s.mission)
        #To save energy
        elif s.mission == self.nFloors and a == 'Keep':
            return State(s.floor, s.doorOpened, s.mission),1
        #Basic rules
        elif a == 'Close':
            return State(s.floor,False,s.mission),-0.04
        elif a == 'Open':
            return State(s.floor,True,s.mission),-0.04
        elif a == 'Down':
            return State(s.floor-1, s.doorOpened, s.mission), -0.04
        elif a == 'Up':
            return State(s.floor+1, s.doorOpened, s.mission), -0.04
        elif a == 'Keep':
            return s, -0.04


        print("Something unexpected happened->",str(s),a)
        return State(agent.pos[1],False,self.nFloors,False), 0

    def getNewMission(self,agent):
        dist = None
        newMission = None
        for p in agent.peopleToLeave:
            d = abs(agent.s.floor - p.goTo)
            if dist == None:
                dist = d
                newMission = p.goTo
            elif d < dist:
                dist = d
                newMission = p.goTo
        return newMission

    def getPeopleByGoTo(self,agent,goTo):
        peopleByGoTo = []
        for p in agent.peopleToLeave:
            if p.goTo == goTo:
                peopleByGoTo.append(p)
        return peopleByGoTo

    def getRewardByDist(self,floor,goTo):
        d = abs(floor - goTo)
        r = 0.8 - (d / (self.nFloors + 1))
        return r

    def saveTimeByPeople(self,people):
        for p in people:
            self.timePeople.append(p.t)