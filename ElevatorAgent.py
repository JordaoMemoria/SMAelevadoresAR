from mesa import Agent
from pandas import DataFrame
from random import randint
from copy import deepcopy, copy

class ElevatorAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.peopleInside = []

        self.lastState = None

        self.s = None
        self.a = None
        self.r = None

        self.w0 = 0
        self.w1 = 1

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
        sl = self.model.getPerception(self.unique_id)
        if self.s != None:
            newQsa = self.Q(self.s,self.a, button) + 1*(self.r + 0.1*self.getMaxVariantionValue(sl, button))
            self.updateWeights(newQsa,button)

        self.s = deepcopy(sl)
        self.a = self.getAction(sl, button)
        self.r = self.model.newAction(self.a,self,button, self.s)

    def getMaxVariantionValue(self,sl, button):
        value = None
        for a in self.model.ACTIONS:
            v = self.Q(sl,a, button) - self.Q(self.s,self.a, button)
            if value == None:
                value = v
            elif v > value:
                value = v
        return value

    def updateWeights(self, newQsa, button):
        lr = 0.4

        if self.a == 'Go':
            a = 1
        else:
            a = -1

        self.w0 += lr * (newQsa - self.Q(self.s, self.a, button))
        self.w1 += lr * (newQsa - self.Q(self.s, self.a, button))*self.getD(self.s,button,self)*a
        #print("Agent", self.unique_id, "w0:", self.w0, "w1:", self.w1)

    def Q(self,s,a, button):
        if a == 'Go':
            av = 1
        elif a == 'Ignore':
            av = -1

        D = self.getD(s,button, self)

        return self.w0 + self.w1*D*av

    def getD(self,s, button, agent):
        ds = [0]*(s.GO.shape[1])
        floorCall, senseCall = self.getFloorAndSenseOfButton(button)
        for i in range(self.s.GO.shape[1]):
            dFloors = 0
            dStops = 0
            a = self.model.schedule.agents[i]
            simulatedFloorsToGo = copy(a.floorsToGo)
            position = s.positions[a.unique_id]

            sense = None

            if len(simulatedFloorsToGo) > 0:
                go = simulatedFloorsToGo[0]
                if position in simulatedFloorsToGo:
                    sense = 0
                elif position > go:
                    sense = -1
                elif position < go:
                    sense = 1
                else:
                    print("Some error happended")
            else:
                sense = 0

            if a.doorsOpened:
                if len(simulatedFloorsToGo) > 0 and simulatedFloorsToGo[0] == position:
                    dFloors -= 1
                elif floorCall == position:
                    dFloors -= 1
                if (position != floorCall and len(simulatedFloorsToGo) > 0 and simulatedFloorsToGo[0] != position) or (len(simulatedFloorsToGo) == 0 and position != floorCall):
                    dFloors += 1

            while position != floorCall:
                if position in simulatedFloorsToGo:
                    dStops += 1
                    simulatedFloorsToGo.remove(position)
                    if len(simulatedFloorsToGo) > 0:
                        if position < simulatedFloorsToGo[0]:
                            sense = 1
                        elif position > simulatedFloorsToGo[0]:
                            sense = -1
                    else:
                        sense = 0
                else:
                    if sense == 1:
                        position += 1
                    elif sense == -1:
                        position -= 1
                    elif sense == 0:
                        if position > floorCall:
                            position -= 1
                            sense = -1
                        elif position < floorCall:
                            position += 1
                            sense = 1
                    dFloors += 1
            sense = 0
            dStops += 1

            if senseCall == 1:
                simulatedFloorsToGo.append(self.model.nFloors -1)
            elif senseCall == -1:
                simulatedFloorsToGo.append(0)
            simulatedFloorsToGo = list(dict.fromkeys(simulatedFloorsToGo))

            while len(simulatedFloorsToGo) > 0:
                if position in simulatedFloorsToGo:
                    if simulatedFloorsToGo[0] != floorCall:
                        dStops += 1
                    simulatedFloorsToGo.remove(position)
                    if len(simulatedFloorsToGo) > 0:
                        if position < simulatedFloorsToGo[0]:
                            sense = 1
                        elif position > simulatedFloorsToGo[0]:
                            sense = -1
                    else:
                        sense = 0
                else:
                    if sense == 1:
                        position += 1
                    elif sense == -1:
                        position -= 1
                    elif sense == 0:
                        if position > simulatedFloorsToGo[0]:
                            position -= 1
                            sense = -1
                        elif position < simulatedFloorsToGo[0]:
                            position += 1
                            sense = 1
                    dFloors += 1




            ds[i] += dFloors + 2*dStops
        #print("Dists:", ds)
        min = 0
        value = ds[0]
        for j in range(len(ds)):
            if ds[j] < value:
                min = j
                value = ds[j]

        if min == agent.unique_id:
            return 1
        else:
            return -1

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
        if e <= 2:
            return action
        else:
            for a in self.model.ACTIONS:
                value = self.Q(sl, a, button)
                if action_value < value:
                    action_value = value
                    action = a
        return action


