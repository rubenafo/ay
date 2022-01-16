import random


class rlist (list):

    def __init__(self, items=[]):
        list.__init__(self, items)

    def rit(self):
        return random.choice(self)

    def rpar(self) -> tuple:
        return self.rit(), self.rit()