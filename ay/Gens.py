import numpy.random
from numpy import random
from ay.plist import plist

class Gens:

    def __init__(self, rnd):
        self.rnd: numpy.random.Generator = rnd

    def ct(x):
        return lambda: x

    @staticmethod
    def shape_alpha():
        return lambda shape: shape.style['stroke'].fA

    def pick (self, arr):
        return plist(arr).rit()

    def norm (self, n, d):
        return self.rnd.normal(n,d)

    def gamm (self, n,d):
        return self.rnd.gamma(n, d)

    def exp (self, v):
        return self.rnd.exponential(v)