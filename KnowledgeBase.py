from pandas import DataFrame
from numpy import zeros

class KnowledgeBase:
    def __init__(self,actions,states):
        lines = len(actions)
        columns = len(states)
        m1 = zeros(shape=(columns, lines))
        m2 = zeros(shape=(columns, lines))
        self.Q = DataFrame(m1, columns=actions, index=states)
        self.Nsa = DataFrame(m2, columns=actions, index=states)