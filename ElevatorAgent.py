from mesa import Agent
from pandas import DataFrame
from random import randint
from copy import deepcopy, copy

class ElevatorAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.peopleInside = []

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
        a = 'Go'
        self.model.newAction(a, self, button)

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


