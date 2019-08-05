import numpy as np
from random import randint

class PoissonGenerator:

    def __init__(self):
        self.sequence = None
        self.sequenceConstant = None
        self.sequenceUp = None
        self.sequenceDown = None
        self.sequenceUpConstant = None
        self.sequenceDownConstant = None

    def setPoissonOrder(self,lamb,segs):
        self.sequence = np.random.poisson(lamb, segs)
        self.sequenceConstant = self.sequence.copy()

    def setUpDownOrder(self,up,down):
        finalAr = []
        for ps in up:
            aux = ps
            n = [0] * 60
            i = 0
            while aux > 0:
                if randint(0, 1) == 1:
                    n[i] += 1
                    aux -= 1
                i += 1
                if i == 60:
                    i = 0
            finalAr.extend(n)
        self.sequenceUp = finalAr
        self.sequenceUpConstant = self.sequenceUp.copy()
        finalAr = []
        for ps in down:
            aux = ps
            n = [0] * 60
            i = 0
            while aux > 0:
                if randint(0, 1) == 1:
                    n[i] += 1
                    aux -= 1
                i += 1
                if i == 60:
                    i = 0
            finalAr.extend(n)
        self.sequenceDown = finalAr
        self.sequenceDownConstant = self.sequenceDown.copy()





    def setSeraratedOrder(self, sequence):
        finalAr = []
        for ps in sequence:
            aux = ps
            n = [0] * 60
            i = 0
            while aux > 0:
                if randint(0,1) == 1:
                    n[i] += 1
                    aux -= 1
                i += 1
                if i == 60:
                    i = 0
            finalAr.extend(n)
        self.sequence = finalAr
        self.sequenceConstant = self.sequence.copy()


    def get_next_second(self):
        if len(self.sequence) > 0:
            first = self.sequence[0]
            self.sequence = np.delete(self.sequence,0)
            return first
        else:
            return 0

    def get_next_second_up_down(self):
        if len(self.sequenceUp) > 0:
            up = self.sequenceUp[0]
            down = self.sequenceDown[0]
            self.sequenceUp = np.delete(self.sequenceUp,0)
            self.sequenceDown = np.delete(self.sequenceDown,0)
            return (up, down)
        else:
            return (0,0)


    def reset(self):
        self.sequence = self.sequenceConstant
        self.sequenceUp = self.sequenceUpConstant
        self.sequenceDown = self.sequenceDownConstant


# T1 = [18,11,15,8,8,34,46,40,34,46,9,10,6,6,9]
#
# p = PoissonGenerator()
# p.setSeraratedOrder(T1)
# print(p.sequenceConstant)
#print(sum(p.sequenceConstant))
