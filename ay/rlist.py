import random
from ay.Point import Point
import numpy as np


class rlist (list[Point]):

    def __init__(self, items=[]):
        list.__init__(self, items)

    def rit(self) -> Point:
        return random.choice(self)

    def rpar(self) -> tuple[Point]:
        return self.rit(), self.rit()

    def head(self) -> Point:
        return self[0]

    def tail(self) -> Point:
        return self[-1]

    def rchunk (self, size: int):
        start = random.randint(len[self] - size)
        return rlist(self[start, start + size])

    def pairs (self) -> list[Point]:
        return rlist(zip(self[::1], self[1::1]))

    def second(self) -> Point:
        assert len(self) >= 2
        return self[1]

    def interpolate (self, step=1):
        pts = self.pairs()
        return np.concatenate(list(map(lambda pair: [pair[0], Point.interpolate(pair[0],pair[1]), pair[1]], pts)))