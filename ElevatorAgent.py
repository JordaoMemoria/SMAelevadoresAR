from mesa import Agent
from pandas import DataFrame
from random import randint

class State:
    def __init__(self, floor, doorOpened, mission):
        self.floor = floor
        self.doorOpened = doorOpened
        self.mission = mission

    def __str__(self):
        return "("+str(self.floor)+","+str(self.doorOpened)+","+str(self.mission)+")"

class ElevatorAgent(Agent):
    def __init__(self, unique_id, model, knowledgeBase):
        super().__init__(unique_id, model)
        self.acting = False

        self.kb = knowledgeBase
        self.s = None
        self.a = None
        self.r = None

        self.peopleToPickUp = []
        self.peopleToLeave = []

#self.kb.Q.at['(0,False,0)','Up'] = 2

    def showAllPeople(self):
        print("Pick Up: ",end='')
        for p in self.peopleToPickUp:
            print(str(p),end='')
        print("Leave: ", end='')
        for p in self.peopleToLeave:
            print(str(p), end='')
        print("")
    def step(self):
        self.updateTimePeople()
        if self.acting:
            self.acting = False
        else:
            self.act()
            self.acting = True

    def act(self):
        #if self.a != None:
        #    print("Elevador", self.unique_id, str(self.s), self.a,end=" | ")
        sl,rl = self.model.getPerception(self.s,self.a,self)
        #print(str(sl),rl)
        #self.showAllPeople()
        if self.s != None:
            self.kb.Nsa.at[str(self.s),self.a] += 1
            self.kb.Q.at[str(self.s),self.a] += 0.9*(rl + 0.1*self.getMaxVariantionValue(sl))
            #self.kb.Q.at[str(self.s), self.a] = rl
        self.s, self.a, self.r = sl, self.getAction(sl,1), rl


    def getMaxVariantionValue(self,sl):
        value = None
        for a in self.model.ACTIONS:
            v = self.kb.Q.at[str(sl),a] - self.kb.Q.at[str(self.s),self.a]
            if value == None:
                value = v
            elif v > value:
                value = v
        return value

    def getAction(self, sl, n):
        default_action = randint(0, len(self.model.ACTIONS)-1)
        action = self.model.ACTIONS[default_action]
        action_value = self.function_exploration(sl, action, n)
        for a in self.model.ACTIONS:
            value = self.function_exploration(sl, a, n)
            if action_value < value:
                action_value = value
                action = a
        return action


    def function_exploration(self, s, a, n):
        if self.kb.Nsa.at[str(s), a] < n:
            return 1
        else:
            return self.kb.Q.at[str(s), a]


    def updateTimePeople(self):
        for p in self.peopleToPickUp:
            p.wait(1)
        for p in self.peopleToLeave:
            p.wait(1)