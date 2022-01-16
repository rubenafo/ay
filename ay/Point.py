import math

import skia


class Point(skia.Point):

    def __init__(self, x=0, y=0):
        skia.Point.__init__(self, x, y)
        self.x = x
        self.y = y

    def cp (self):
        return Point(self.x, self.y)

    def add (self, x=0, y=0):
        self.x += x
        self.y += y
        return self

    @staticmethod
    def tang (p0, p1, p2, p3, width):
        t = 0.5
        t1 = t - 1.0
        x = 0.5 * (3 * t1 * (p1.x * t1 - p2.x * t) + p3.x * t * t) - p0.x * t1 * t1 * t1
        y = 0.5 * (3 * t1 * (p1.y * t1 - p2.y * t) + p3.y * t * t) - p0.y * t1 * t1 * t1
        tx = 3*t*t * (-p0.x+3*p1.x-3*p2.x+p3.x) + 6*t * (p0.x-2*p1.x+p2.x) + 3 * (-p0.x+p1.x)
        ty = 3*t*t * (-p0.y+3*p1.y-3*p2.y+p3.y) + 6*t * (p0.y-2*p1.y+p2.y) + 3 * (-p0.y+p1.y)
        a = math.atan2(y, x)
        a -= math.pi/2
        return Point(math.cos(a) * width +x, math.sin(a) * width + y)

    @staticmethod
    def point_at (a, b, c, d, t: float):
        t1 = t - 1.0
        px = t * (3*t1*(b.x*t1-c.x*t) + d.x*t*t) - a.x*t1*t1*t1
        py = t * (3*t1*(b.y*t1-c.y*t) + d.y*t*t) - a.y*t1*t1*t1
        return Point(px, py)

    @staticmethod
    def angle (p0, p1):
        xDiff = p0.x - p1.x
        yDiff = p0.y - p1.y
        return math.atan2(yDiff, xDiff) * (180 / math.pi)

    @staticmethod
    def rotate (p, around, deg: float):
        radians = deg * math.pi / 180
        cos = math.cos(radians)
        sin = math.sin(radians)
        dx = p.x - around.x
        dy = p.y - around.y
        newx = cos * dx - sin * dy + around.x
        newy = sin * dx + cos * dy + around.y
        return Point(newx, newy)

    @staticmethod
    def off (p0, p1, offset: float):
        p = p1.copy().sub(0, offset)
        angle = Point.angle(p0, p1)
        return Point.rotate(p, p1, angle)