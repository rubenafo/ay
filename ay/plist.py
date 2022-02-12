import numpy
from numpy import random

from ay.Point import Point


class plist (list[Point]):

    def __init__(self, items: list =[], seed: int=0):
        list.__init__(self, items)
        self.seed = seed
        self.rnd: random.Generator = numpy.random.default_rng(seed)

    def rit(self) -> Point:
        return self.rnd.choice(self)

    def rits (self, num: int = 3):
        return plist(items=[self.rit() for i in range(0, num)])

    def rpar(self) -> tuple[Point]:
        return self.rit(), self.rit()

    def head(self) -> Point:
        return self[0]

    def tail(self) -> Point:
        return self[-1]

    def rchunk (self, size: int):
        start = self.rnd.integers(0, len(self) - size)
        return plist(self[start:start + size])

    def pairs (self, link=0) -> list[Point]:
        return plist(zip(self[::1], self[1::1]))

    def second(self) -> Point:
        assert len(self) >= 2
        return self[1]

    def as_tuples (self) -> list:
        return [(s.x, s.y) for s in self]

    def closest (self, p: Point) -> Point:
        dists = [Point.distance(p, pt) for pt in self if p != pt]
        cl = min(dists)
        return self[dists.index(cl)]

    def furthest (self, p: Point) -> Point:
        dists = [Point.distance(p, pt) for pt in self if p != pt]
        cl = max(dists)
        return self[dists.index(cl)]

    def chunks (self, size=1, overlap=0):
        chks = [self[i:i+size] for i in range(0, len(self)-size+1, size)]
        if overlap > 0:
            for i in range(1, len(chks)):
                chks[i][0:0] = chks[i-1][-overlap:]
        return plist(chks)
