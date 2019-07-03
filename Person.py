
class Person:
    def __init__(self,floor,goTo):
        self.floor = floor
        self.goTo = goTo
        self.t = 0

    def wait(self):
        self.t += 1

    def __str__(self):
        return '['+str(self.floor)+str(self.goTo)+']'
