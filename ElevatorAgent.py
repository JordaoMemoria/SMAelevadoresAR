from mesa import Agent

class ElevatorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.acting = False
        self.mission = 0
        self.doorOpened = False


    def step(self):
        if self.acting:
            self.acting = False
        else:
            self.act()
            self.acting = True

    def act(self):
        print("Elevador", self.unique_id, "("+str(self.pos[1])+","+str(self.doorOpened)+",",str(self.mission)+")")