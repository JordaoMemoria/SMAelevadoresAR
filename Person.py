
class Person:
    def __init__(self,floor,goTo):
        self.floor = floor
        self.goTo = goTo
        self.tWait = 0
        self.tJourney = 0
        self.elevatorsGoing = 0

    def wait(self,segs):
        self.tWait += segs

    def journey(self,segs):
        self.tJourney += segs

    def __str__(self):
        return '['+str(self.floor)+str(self.goTo)+']'

    def getReward(self):
        return ((self.floor - self.goTo)**3)/self.t
