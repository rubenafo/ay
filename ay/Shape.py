import skia
from ay.Point import Point
import colour


class Shape:

    def __init__(self):
        self.head: Point = Point()
        self.points: list[tuple(Point, Point, Point)] = []
        self.closed = False
        self.zindex = 0
        self.style = {} # fill, stroke, stroke_width

    def fill (self, fill: str, alpha=1):
        color: colour.Color = colour.hex2rgb(fill)
        self.style['fill'] = skia.Color4f(color[0], color[1], color[2], alpha)
        return self


    def stroke (self, stroke_color: str, alpha=1, stroke_width=5):
        color: colour.Color = colour.hex2rgb(stroke_color)
        self.style['stroke'] = skia.Color4f(color[0], color[1], color[2], alpha)
        self.style['stroke_width'] = stroke_width if stroke_width else None
        return self

    @staticmethod
    def line (p0: Point = (0,0), p1: Point = (0,0)):
        s = Shape()
        p0 = p0 if type(p0) == Point else Point(p0[0], p0[1])
        p1 = p1 if type(p1) == Point else Point(p1[0], p1[1])
        s.head = p0
        s.points = [(p0, p1, p1)]
        s.closed = True
        return s

    def draw(self) -> skia.Path:
        path = skia.Path()
        path.moveTo(self.head.x, self.head.y)
        for seg in self.points:
            path.cubicTo(seg[0].x, seg[0].y+30, seg[1].x, seg[1].y, seg[2].x, seg[2].y)
        path.close() if self.closed else None
        return path
