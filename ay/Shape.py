
import colour
import numpy as np
from skia import Path, Color4f

from ay import Canvas, Utils
from ay.Point import Point
from ay.Utils import resolve
from ay import Shapes


class Shape:

    def __init__(self, start_point: Point = None):
        self.head = start_point if start_point else None
        self.segments: list = []
        self.closed = False
        self.zindex = 0
        self.style = {} # fill, stroke, stroke_width

    def tail(self) -> Point:
        return self.segments[-1]['p2']

    def addPoint(self, p: Point):
        last_point = self.tail()
        self.segments.append({'c1': p, 'c2': last_point, 'p2': p})
        return self

    def add(self, p0: Point, p1: Point, p2: Point):
        self.segments.append({'c1': p0, 'c2': p1, 'p2': p2})
        return self

    def close (self):
        self.closed = True
        return self

    def fill(self, fill: str, alpha=1):
        fill = resolve(fill)
        alpha = resolve(alpha)
        color: colour.Color = colour.hex2rgb(fill)
        self.style['fill'] = Color4f(color[0], color[1], color[2], alpha)
        return self

    def stroke (self, color: str, alpha=1, width=5):
        stroke_color = resolve(color)
        alpha = resolve(alpha)
        stroke_width = resolve(width)
        color: colour.Color = colour.hex2rgb(stroke_color)
        self.style['stroke'] = Color4f(color[0], color[1], color[2], alpha)
        self.style['stroke_width'] = stroke_width if stroke_width else None
        return self

    @staticmethod
    def line (p0: Point = (0,0), p1: Point = (0,0)):
        p0 = p0 if type(p0) == Point else Point(p0[0], p0[1])
        p1 = p1 if type(p1) == Point else Point(p1[0], p1[1])
        return Shapes.curve(p0, p0, p1, p1)

    def draw(self) -> Path:
        path = Path()
        path.moveTo(self.head)
        for seg in self.segments:
            path.cubicTo(seg['c1'],seg['c2'],seg['p2'])
        path.close() if self.closed else None
        return path

    def rotate(self, deg: float, origin: Point = None):
        points = [self.head]
        points.extend(np.concatenate([[s['c1'], s['c2'], s['p2']] for s in self.segments]))
        points = list(map(lambda p: (p.x, p.y), points))
        origin = self.center() if origin is None else origin
        origin = (origin.x, origin.y)
        angle = np.deg2rad(deg)
        r = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)]])
        o = np.atleast_2d(origin)
        p = np.atleast_2d(points)
        rotpoints = np.squeeze((r.dot(p.T - o.T) + o.T).T)
        self.head = Point(rotpoints[0][0], rotpoints[0][1])
        self.segments.clear()
        for i in range(1, len(rotpoints)-2, 3):
            c1 = Point(rotpoints[i][0], rotpoints[i][1])
            c2 = Point(rotpoints[i+1][0], rotpoints[i+1][1])
            p2 = Point(rotpoints[i+2][0], rotpoints[i+2][1])
            self.segments.append({'c1':c1, 'c2':c2, 'p2':p2})
        return self

    def center(self) -> Point:
        points = [self.head] + [s['p2'] for s in self.segments]
        x = np.average([p.x for p in points])
        y = np.average([p.y for p in points])
        return Point(x,y)

    def translate(self, p:Point):
        self.head = self.head + p
        for seg in self.segments:
            seg['c1'] = seg['c1'] + p
            seg['c2'] = seg['c2'] + p
            seg['p2'] = seg['p2'] + p
        return self

    def cp(self):
        new_shape = Shape()
        new_shape.head = self.head.cp()
        new_shape.segments = [{'c2': s['c2'], 'c1':s['c1'], 'p2':s['p2']}
                              for s in self.segments]
        new_shape.closed = self.closed
        new_shape.zindex = self.zindex
        new_shape.style = self.style.copy()
        return new_shape

    def subd(self, t: float):
        prev_p1 = self.head
        new_segs = []
        for seg in self.segments:
            a = prev_p1
            d = seg['p2']
            b = seg['c1']
            c = seg['c2']
            e = ((b - a) * t) + a
            f = ((c - b) * t) + b
            g = ((d - c) * t) + c
            h = ((f - e) * t) + e
            j = ((g - f) * t) + f
            k = ((j - h) * t) + h
            new_segs.append({'c1': e, 'c2': h, 'p2': k})
            new_segs.append({'c1': j, 'c2': g, 'p2': d})
            prev_p1 = d
        self.segments = new_segs
        return self

    def reg(self, canvas: Canvas):
        canvas.add(self)
        return self

    def cpoints(self) -> list[Point]:
        return [self.head] + [seg['p2'] for seg in self.segments]

    def adjust (self):
        for i in range (1, len(self.segments)):
            s0 = self.segments[i-1]
            d = Point.distance(s0['c2'], s0['p2'])
            nc1 = Utils.proj(s0['c2'], s0['p2'], 2*d)
            self.segments[i]['c1'] = nc1
        return self

    def noise (self, func):
        self.head = func(self, self.head)
        for index, seg in enumerate(self.segments):
            func(index, seg)
        return self
