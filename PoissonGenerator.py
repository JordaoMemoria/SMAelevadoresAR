import numpy as np


class PoissonGenerator:
    def __init__(self, lamb, segs):
        self.sequence = np.random.poisson(lamb, segs)

    def get_next_second(self):
        first = self.sequence[0]
        self.sequence = np.delete(self.sequence,0)
        return first



