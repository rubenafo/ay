import skia
from numpy import cos, sin

from ay.Point import Point
import colour
from ay.Utils import resolve
import numpy as np


class Shape:

    def __init__(self):
        self.pxs: list = []
        self.pys: list = []
        self.closed = False
        self.zindex = 0
        self.style = {} # fill, stroke, stroke_width

    def tail(self):
        return self.pxs[-1], self.pys[-1]

    def addPoint(self, p: Point):
        last_point = self.tail()
        self.pxs.extend([last_point[0], p.x, p.x])
        self.pys.extend([last_point[1], p.y, p.y])
        return self

    def add(self, p0: Point, p1: Point, p2: Point):
        self.pxs.append(p0.x, p1.x, p2.x)
        self.pys.append(p0.y, p1.y, p2.y)
        return self

    def close (self):
        self.closed = True
        return self

    def fill(self, fill: str, alpha=1):
        fill = resolve(fill)
        alpha = resolve(alpha)
        color: colour.Color = colour.hex2rgb(fill)
        self.style['fill'] = skia.Color4f(color[0], color[1], color[2], alpha)
        return self

    def stroke (self, stroke_color: str, alpha=1, stroke_width=5):
        stroke_color = resolve(stroke_color)
        alpha = resolve(alpha)
        stroke_width = resolve(stroke_width)
        color: colour.Color = colour.hex2rgb(stroke_color)
        self.style['stroke'] = skia.Color4f(color[0], color[1], color[2], alpha)
        self.style['stroke_width'] = stroke_width if stroke_width else None
        return self

    @staticmethod
    def curve (p0: Point, p1: Point, p2: Point, p3: Point):
        s = Shape()
        p0 = p0 if type(p0) == Point else Point(p0[0], p0[1])
        p1 = p1 if type(p1) == Point else Point(p1[0], p1[1])
        p2 = p2 if type(p2) == Point else Point(p2[0], p2[1])
        p3 = p3 if type(p3) == Point else Point(p3[0], p3[1])
        s.pxs = [p0.x, p1.x, p2.x, p3.x]
        s.pys = [p0.y, p1.y, p2.y, p3.y]
        s.closed = False
        return s

    @staticmethod
    def line (p0: Point = (0,0), p1: Point = (0,0)):
        p0 = p0 if type(p0) == Point else Point(p0[0], p0[1])
        p1 = p1 if type(p1) == Point else Point(p1[0], p1[1])
        return Shape.curve(p0, p0, p1, p1)

    @staticmethod
    def rect (x: float, y: float, width: float, height: float):
        p0 = Point(x,y)
        p1 = Point (p0.x+width, p0.y)
        p2 = Point (p1.x, p1.y + height)
        p3 = Point (p0.x, p0.y + height)
        return Shape.line(p0, p1).addPoint(p2).addPoint(p3).close()

    def draw(self) -> skia.Path:
        path = skia.Path()
        path.moveTo(self.pxs[0], self.pys[0])
        for i in range(1, len(self.pxs)-2, 2):
            path.cubicTo(self.pxs[i], self.pys[i],
                         self.pxs[i+1], self.pys[i+1],
                         self.pxs[i+2], self.pys[i+2])
        path.close() if self.closed else None
        return path

    def rotate(self, deg: float, origin: Point = None):
        points =[(self.pxs[i], self.pys[i]) for i in range (0, len(self.pxs))]
        origin = self.center() if origin is None else origin
        origin = (origin.x, origin.y)
        angle = np.deg2rad(deg)
        r = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)]])
        o = np.atleast_2d(origin)
        p = np.atleast_2d(points)
        rotpoints = np.squeeze((r.dot(p.T - o.T) + o.T).T)
        self.pxs = [p[0] for p in rotpoints]
        self.pys = [p[1] for p in rotpoints]
        return self

    def center (self) -> Point:
        x = np.average([self.pxs[i] for i in range (0, len(self.pxs), 3)])
        y = np.average([self.pys[i] for i in range (0, len(self.pys), 3)])
        return Point(x,y)
