import math
import numpy as np
import skia

from ay import Utils


class Point(skia.Point):

    def __init__(self, *args):
        skia.Point.__init__(self, *args)
        self.x = self.x()
        self.y = self.y()

    def __sub__(self, other):
        p = skia.Point.__sub__(self, other)
        return Point(p.x(), p.y())

    def __mul__(self, other):
        p = skia.Point.__mul__(self, other)
        return Point(p.x(), p.y())

    def __add__(self, other):
        p = skia.Point.__add__(self, other)
        return Point(p.x(), p.y())

    def __truediv__(self, other):
        other = other if type(other) == Point else Point(other, other)
        return Point(self.x/other.x, self.y/other.y)

    def cp (self):
        return Point(self.x, self.y)

    def add (self, x=0, y=0):
        self.x += x
        self.y += y
        return self

    @staticmethod
    def mid (p0, p1):
        return (p0 + p1)/2

    @staticmethod
    def tang (p0, p1, p2, p3, width):
        bp = Utils.bezier_point(p0, p1, p2, p3, width)
        t = Utils.bezier_tangent(p0, p1, p2, p3, width)
        a = np.math.atan2(t.y, t.x)
        a -= np.pi/2
        return Point(np.cos(a) * width + bp.x, np.sin(a) * width + bp.y)

    @staticmethod
    def point_at (a, b, c, d, t: float):
        return Utils.bezier_point(a, b, c, d, t)

    @staticmethod
    def angle (p0, p1):
        xdiff = p1.x - p0.x
        ydiff = p1.y - p0.y
        return np.math.atan2(ydiff, xdiff) * (180 / np.pi)

    @staticmethod
    def rotate (p, around, deg: float):
        radians = deg * np.pi / 180
        cos = np.cos(radians)
        sin = np.sin(radians)
        dx = p.x - around.x
        dy = p.y - around.y
        newx = cos * dx - sin * dy + around.x
        newy = sin * dx + cos * dy + around.y
        return Point(np.round(newx,2), np.round(newy,2))

    @staticmethod
    def off (p0, p1, offset: float):
        p = p0 - Point(0, offset)
        angle = Point.angle(p0, p1)
        return Point.rotate(p, p0, angle)

    @staticmethod
    def interpolate (p0, p1, step=0.5):
        x = p0.x + (p1.x - p0.x) * step
        y = p0.y + (p1.y - p0.y) * step
        return Point(x, y)

    @staticmethod
    def distance (p0, p1):
        return Point.Distance(skia.Point(p0.x, p0.y), skia.Point(p1.x, p1.y))

