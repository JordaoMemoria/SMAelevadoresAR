
class Person:
    def __init__(self,floor,goTo):
        self.floor = floor
        self.goTo = goTo
        self.t = 0
        self.elevatorsGoing = 0

    def wait(self,segs):
        self.t += segs

    def __str__(self):
        return '['+str(self.floor)+str(self.goTo)+']'

    def getReward(self):
        return ((self.floor - self.goTo)**3)/self.t
