import skia


class Point(skia.Point):

    def __init__(self, x=0, y=0):
        skia.Point.__init__(self, x, y)
        self.x = x
        self.y = y