from mesa import Agent
from random import randint
from Person import Person

class PeopleSimulator(Agent):
    def __init__(self, unique_id, model, poisonGenerator, agents):
        super().__init__(unique_id, model)
        self.poissonGenerator = poisonGenerator
        self.peopleWaitingOnFloors = []
        self.people = []
        self.agents = agents

    def showPeople(self):
        print("People waiting: ", end='')
        for p in self.people:
            print(str(p),end=' ')
        print("")

    def step(self):
        self.updateTimePeople()

        for p in self.people:
            if p.elevatorsGoing == 0:
                self.updateState(p,1)

        nPeopleJustArrive = self.poissonGenerator.get_next_second()
        for i in range(nPeopleJustArrive):
            p = self.ordinary()
            self.people.append(p)
            #print(" -------------->>>>>>>>>>>   People just arrive at floor", str(p))
            self.updateState(p,1)


    def ordinary(self):
        newP = randint(0, self.model.nFloors - 1)
        p = Person(newP, self.sortGoTo(newP))
        return p

    def downPeak(self):
        newP = randint(1, self.model.nFloors - 1)
        p = Person(newP, 0)
        return p

    def upPeak(self):
        newP = randint(1, self.model.nFloors - 1)
        p = Person(0,newP)
        return p


    def updateState(self,person, value):

        p = randint(1,10)
        if p <= 7:
            if person.floor == 0:
                self.model.currentState.buttons[0] = value
                for a in self.agents:
                    a.idButtons.append(0)
            elif person.floor == self.model.nFloors-1:
                self.model.currentState.buttons[-1] = value
                for a in self.agents:
                    a.idButtons.append(2*self.model.nFloors-3)
            elif person.floor > person.goTo:
                self.model.currentState.buttons[2*person.floor-1] = value
                for a in self.agents:
                    a.idButtons.append(2*person.floor-1)
            elif person.floor < person.goTo:
                self.model.currentState.buttons[2*person.floor] = value
                for a in self.agents:
                    a.idButtons.append(2*person.floor)
        else:
            elevator_id = randint(0,len(self.agents)-1)
            if person.floor == 0:
                self.model.currentState.buttons[0] = value
                for a in self.agents:
                    if a.unique_id == elevator_id:
                        a.idButtons.append(0)
            elif person.floor == self.model.nFloors-1:
                self.model.currentState.buttons[-1] = value
                for a in self.agents:
                    if a.unique_id == elevator_id:
                        a.idButtons.append(2*self.model.nFloors-3)
            elif person.floor > person.goTo:
                self.model.currentState.buttons[2*person.floor-1] = value
                for a in self.agents:
                    if a.unique_id == elevator_id:
                        a.idButtons.append(2*person.floor-1)
            elif person.floor < person.goTo:
                self.model.currentState.buttons[2*person.floor] = value
                for a in self.agents:
                    if a.unique_id == elevator_id:
                        a.idButtons.append(2*person.floor)

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
        self.people = [p for p in self.people if p not in peopleByFloor]
        return peopleByFloor

    def setPeopleByFloorWithElevators(self,floor):
        for p in self.people:
            if p.floor == floor:
                p.elevatorsGoing += 1

    def updateTimePeople(self):
        for p in self.people:
            p.wait(1)