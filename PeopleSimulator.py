from mesa import Agent
from random import randint
from Person import Person

class PeopleSimulator(Agent):
    def __init__(self, unique_id, model, poisonGenerator):
        super().__init__(unique_id, model)
        self.poissonGenerator = poisonGenerator
        self.peopleWaitingOnFloors = []
        self.people = []

    def showPeople(self):
        for p in self.people:
            print(str(p),end=' ')
        print("")

    def step(self):
        self.updateTimePeople()
        nPeopleJustArrive = self.poissonGenerator.get_next_second()
        for i in range(nPeopleJustArrive):
            newP = randint(0,self.model.nFloors-1)
            p = Person(newP,self.sortGoTo(newP))
            self.people.append(p)
            print("People just arrive at floor", str(p))
            self.updateState(p)

    def updateState(self,person):
        if person.floor == 0:
            self.model.currentState.buttons[0] = 1
        elif person.floor == self.model.nFloors-1:
            self.model.currentState.buttons[-1] = 1
        elif person.floor > person.goTo:
            self.model.currentState.buttons[2*person.floor-1] = 1
        elif person.floor < person.goTo:
            self.model.currentState.buttons[2*person.floor] = 1

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

    def updateTimePeople(self):
        for p in self.people:
            p.wait(1)