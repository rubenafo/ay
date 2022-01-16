import numpy.random
from numpy import random
from ay.rlist import rlist

class Gens:

    def __init__(self, rnd):
        self.rnd: numpy.random.Generator = rnd

    def ct(x):
        return lambda: x

    def pick (self, arr):
        return rlist(arr).rit()

    def norm (self, n, d):
        return self.rnd.normal(n,d)

    def gamm (self, n,d):
        return self.rnd.gamma(n, d)

    def exp (self, v):
        return self.rnd.exponential(v)