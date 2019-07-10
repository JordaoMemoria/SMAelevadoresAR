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

        self.w0 = 0.1
        self.w1 = 0.1

        self.floorsToGo = []
        self.doorsOpened = False

        self.idButtons = []

    def showPeople(self):
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
            for i in self.idButtons:
                self.qlearningAction(i)
            self.idButtons = []

    def someNewButtonWasPressed(self):
        if len(self.idButtons) > 0:
            return True
        else:
            return False

    def qlearningAction(self,button):
        sl,rl = self.model.getPerception(self.unique_id)
        print("----------------------------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Agente",self.unique_id,rl)
        if self.s != None:
            newQsa = self.Q(self.s,self.a, button) + 0.9*(rl + 0.9*self.getMaxVariantionValue(sl, button))

        self.s = deepcopy(sl)
        self.a = self.getAction(sl, button)
        self.model.newAction(self.a,self,button)

    def getMaxVariantionValue(self,sl, button):
        value = None
        for a in self.model.ACTIONS:
            v = self.Q(sl,a, button) - self.Q(self.s,self.a, button)
            if value == None:
                value = v
            elif v > value:
                value = v
        return value

    def Q(self,s,a, button):
        if a == 'Go':
            av = 1
        elif a == 'Ignore':
            av = -1

        D = self.getD(s, button)

        return self.w0 + self.w1*D*av

    def getD(self,s, button):
        ds = [1,1,1]
        print(button, self.getFloorAndSenseOfButton(button))
        for i in range(self.s.GO.shape[1]):
            a = self.model.schedule.agents[i]

        return 0

    def getFloorAndSenseOfButton(self, button):
        floor = int((button+1)/2)
        if ((button+1)/2)%1 == 0:
            sense = -1
        else:
            sense = 1
        return (floor, sense)

    def getAction(self, sl, button):

        default_action = randint(0, len(self.model.ACTIONS)-1)
        #default_action = 0
        action = self.model.ACTIONS[default_action]
        action_value = self.Q(sl, action, button)

        e = randint(1,10)
        if e < 3:
            return action
        else:
            for a in self.model.ACTIONS:
                value = self.Q(sl, a, button)
                if action_value < value:
                    action_value = value
                    action = a
        return action


