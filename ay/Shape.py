import pixie
import skia

from ay.Point import Point

class Shape:

    def __init__(self):
        self.head: Point = Point()
        self.points: list[tuple(Point, Point, Point)] = []
        self.closed = False
        self.zindex = 0
        self.style = {}

    def style (st):
        None

    @staticmethod
    def line (p0: Point = (0,0), p1: Point = (0,0)):
        s = Shape()
        p0 = p0 if type(p0) == Point else Point(p0[0], p0[1])
        p1 = p1 if type(p1) == Point else Point(p1[0], p1[1])
        s.head = p0
        s.points = [(p0, p1, p1)]
        s.closed = True
        return s

    def draw(self) -> pixie.Path:
        path_str = "M {},{} ".format(self.head.x, self.head.y)
        for seg in self.points:
            chunk = "C {},{} {},{} {},{} ".format(
                seg[0].x, seg[0].y, seg[1].x, seg[1].y, seg[2].x, seg[2].y)
            path_str += chunk
        path_str += "Z" if self.closed else None
        path = pixie.parse_path(path_str)
        return path