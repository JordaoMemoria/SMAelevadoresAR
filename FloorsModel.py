from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ElevatorAgent import ElevatorAgent
from ControllerAgent import ControllerAgent
from PoissonGenerator import PoissonGenerator

class FloorsModel(Model):
    def __init__(self, nElevators, nFloors, lamb):
        self.nElevators = nElevators
        self.nFloors = nFloors
        self.grid = MultiGrid(1, nFloors, False)
        self.schedule = RandomActivation(self)

        for i in range(self.nElevators):
            a = ElevatorAgent(i, self)
            self.schedule.add(a)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (0, y))

        pg = PoissonGenerator(lamb, 86400)
        self.controllerAgent = ControllerAgent(i+1, self, self.schedule.agents, pg)
        self.schedule.add(self.controllerAgent)

    def step(self):
        # This steps represents 1 second
        self.schedule.step()




