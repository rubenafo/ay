from typing import List

import cairo
from colour import Color

from ay import Point, PPoint
from ay.Canvas import Canvas

def resolve_cal(x):
    return x() if callable(x) else x

class Shape:

    def __init__(self, start: Point, closed=False):
        startv = resolve_cal(start)
        self.start = startv if type(startv) == Point else Point(startv)
        self.points: List[Point] = []
        self.closed = False
        self.style = {'fill':'black', 'opacity':1, 'stroke':'black', 'stroke_width':0, 'stroke_opacity':1,
                      'line_cap': cairo.LineCap.SQUARE,
                      'blend': cairo.OPERATOR_COLOR_BURN}

    def add(self, c1, c2, p):
        p1 = Point(c1) if isinstance(c1, tuple) else c1
        p2 = Point(c2) if isinstance(c2, tuple) else c2
        p = Point(p) if isinstance(p, tuple) else p
        self.points.append([p1, p2, p])
        return self

    def blend(self, blendMode):
        self.style['blend'] = blendMode
        return self

    def close(self):
        self.isclosed = True
        return self

    def fill (self, fill, opacity=1):
        self.style['fill'] = fill
        self.style['opacity'] = opacity
        return self

    def stroke(self, stroke, width=1, opacity=1):
        self.style['stroke'] = stroke
        self.style['stroke_width'] = width
        self.style['stroke_opacity'] = opacity
        return self

    def line_cap (self, cap: cairo.LineCap):
        self.style['line_cap'] = cap
        return self

    def drawTo(self, canvas: Canvas):
        canvas.context.move_to(self.start.x, self.start.y)
        for p in self.points:
            canvas.context.curve_to(p[0].x, p[0].y, p[1].x, p[1].y, p[2].x, p[2].y)
        if self.closed:
            canvas.context.close_path()
        canvas.context.set_operator(self.style['blend'])
        if self.style['fill']:
            color = Color(self.style["fill"])
            canvas.context.set_source_rgba(color.get_red(), color.get_green(), color.get_blue() , self.style["opacity"])
            canvas.context.fill_preserve()
        if self.style['line_cap']:
            canvas.context.set_line_cap(self.style['line_cap'])
        if self.style['stroke']:
            stroke_color = Color(self.style['stroke'])
            canvas.context.set_line_width(self.style['stroke_width'])
            canvas.context.set_source_rgba(stroke_color.get_red(), stroke_color.get_green(), stroke_color.get_blue(),
                                           resolve_cal(self.style['stroke_opacity']))
            canvas.context.stroke()
        return self

    def subd (self, t):
        pts = [self.start]
        pts += list(sum((self.points), []))
        nps = []
        for i in range(0, len(pts)-3, 3):
            a, d, b, c = pts[i], pts[i+3], pts[i+1], pts[i+2]
            e = ((b - a) * t) + a
            f = ((c - b) * t) + b
            g = ((d - c) * t) + c
            h = ((f - e) * t) + e
            j = ((g - f) * t) + f
            k = ((j - h) * t) + h
            nps += [e,h,k,j,g,d]
        self.points = [nps[i:i+3] for i in range(0, len(nps), 3)]
        return self

    def noise (self, f):
        pts = [self.start] + sum(self.points, [])
        noisy_pts = [pt.noise(f) for pt in pts]
        self.start = noisy_pts[0]
        self.points = [noisy_pts[i:i+3] for i in range(1, len(noisy_pts), 3)]
        #self.points[-1] = [self.points[-1][0], self.start, self.start]
        return self

    def trans (self, d):
        self.start = self.start + d
        for i in range(0, len(self.points)):
            segment = self.points[i]
            self.points[i] = [p + d for p in segment]
        return self

    def adjust(self):
        for i in range(1, len(self.points)):
            p0 = self.points[i-1]
            p1 = self.points[i]
            d =  p0[1].distance(p0[2])
            np2 = Point.proj(p0[1], p0[2], d*2)
            self.points[i] = [np2, p1[1], p1[2]]
        return self

    @staticmethod
    def rect (pt: Point, width: float, height: float):
        pt = resolve_cal(pt)
        p = Point(pt) if isinstance(pt, tuple) else pt
        s = Shape(p)\
            .add(p, p + (width,0), p + (width,0))\
            .add(p + (width, 0), p + (width, height), p + (width, height))\
            .add(p + (width, height), p + (0, height), p + (0, height))\
            .add(p + (0, height), p, p)
        return s

    @staticmethod
    def circle (pt: Point, r: float):
        c = 0.5522847498307933984022516322796;
        shape = Shape(pt + (0, -r))
        shape.add(Point(c*r, -r) + pt, Point(r,-c*r) + pt,  Point(r,0) + pt)
        shape.add(Point(r, c * r) + pt, Point(c * r, r) + pt, Point(0, r) + pt)
        shape.add(Point(-c * r, r) + pt, Point(-r, c * r) + pt, Point(-r, 0) + pt)
        shape.add(Point(-r, -c * r) + pt, Point(-c * r, -r) + pt, Point(0, -r) + pt)
        return shape
