from numpy import zeros

class State:
    def __init__(self, p_elevators, m_floors):
        self.n_elevators = len(p_elevators)
        self.m_floors = m_floors
        self.positions = p_elevators
        self.senses = [0] * len(p_elevators)
        self.buttons = [0] * (2 * m_floors - 2)
        self.GO = zeros((self.m_floors, self.n_elevators))
        self.LEAVE = zeros((self.m_floors, self.n_elevators))

    def __str__(self):
        return "Positions "+str(self.positions)+"\nSenses    "+str(self.senses)+"\nButtons   "+str(self.buttons)+"\nGo calls\n"+str(self.GO)+"\nLeaving\n"+str(self.LEAVE)
