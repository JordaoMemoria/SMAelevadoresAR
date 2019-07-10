from mesa import Agent
from pandas import DataFrame
from random import randint
from copy import deepcopy

class ElevatorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.peopleInside = []

        self.lastState = None

        self.s = None
        self.a = None
        self.r = None

        self.w0 = 0.1
        self.w1 = 0.1

    def initLastState(self):
        self.lastState = deepcopy(self.model.currentState)

    def showAllPeople(self):
        print("People inside: ", end='')
        for p in self.peopleInside:
            print(str(p), end='')
        print("")

    def updateTimePeople(self):
        for p in self.peopleInside:
            p.wait(1)

    def step(self):
        self.updateTimePeople()
        if self.someNewButtonWasPressed():
            for i in range(len(self.lastState.buttons)):
                if self.lastState.buttons[i] != self.model.currentState.buttons[i]:
                    self.qlearningAction(i)

    def someNewButtonWasPressed(self):
        if self.lastState.buttons == self.model.currentState.buttons:
            return False
        else:
            return True

    def qlearningAction(self,button):
        sl,rl = self.model.getPerception()
        # if self.s != None:
        #     newQsa = self.Q(self.s,self.a) + 0.9*(r + 0.9*self.getMaxVariantionValue(sl))
        self.s, self.r = deepcopy(sl), rl
        self.a = self.getAction(sl)
        self.model.newAction(self.a,self,button)

    def getMaxVariantionValue(self,sl):
        value = None
        for a in self.model.ACTIONS:
            v = self.Q(sl,a) - self.Q(self.s,self.a)
            if value == None:
                value = v
            elif v > value:
                value = v
        return value

    def Q(self,s,a):
        return 0

    def getAction(self, sl):

        default_action = randint(0, len(self.model.ACTIONS)-1)
        action = self.model.ACTIONS[default_action]
        action_value = self.Q(sl, action)

        e = randint(1,10)
        if e < 0:
            return action
        else:
            for a in self.model.ACTIONS:
                value = self.Q(sl, a)
                if action_value < value:
                    action_value = value
                    action = a
        return action


