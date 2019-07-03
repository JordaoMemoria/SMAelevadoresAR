import numpy as np


class PoissonGenerator:
    def __init__(self, lamb, segs):
        self.sequence = np.random.poisson(lamb, segs)
        self.sequenceContant = self.sequence.copy()

    def get_next_second(self):
        if len(self.sequence) > 0:
            first = self.sequence[0]
            self.sequence = np.delete(self.sequence,0)
            return first
        else:
            return 0

    def reset(self):
        self.sequence = self.sequenceContant
