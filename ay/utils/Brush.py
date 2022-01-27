from ay import Utils, Shapes
from ay.Point import Point
from ay.Shape import Shape
from ay.plist import plist


class Brush:

    def __init__(self, points):
        self.center = points
        self.left = []
        self.right = []

    def contour_points(self, points: list[Point], width: float):
        outer = []
        inner = []
        outer.append(Point.off(points[0], points[1], width))
        inner.append(Point.off(points[0], points[1], -width))
        pairs = list(zip(points[::1], points[1::1]))
        for i in range(0, len(pairs)):
            pair = pairs[i]
            p1 = Point.off(pair[1], pair[0], -width)
            p2 = Point.off(pair[1], pair[0], width)
            #if i < len(pairs)-1:
            #    nxt = pairs[i+1][0]
            #    p1 = Point.rotate(p1, pair[1], Point.angle(pair[1], nxt))
            #    p2 = Point.rotate(p2, pair[1], Point.angle(pair[1], nxt))
            outer.append(p1)
            inner.append(p2)
        self.left = outer
        self.right = inner
        return outer,inner

    def linear(self, outer: list[Point], inner: list[Point]):
        shape = Shape(outer[0])
        for i in range (1, len(outer)):
            start = outer[i-1]
            end = outer[i]
            d = Point.distance(start, end)
            shape.add(Utils.proj(start, end, d/3), Utils.proj(start, end, 2*d/3), end)
        last_innpoint = inner[-1]
        d = Point.distance (end, last_innpoint)
        shape.add(Utils.proj(end, last_innpoint, d / 3),
                  Utils.proj(end, last_innpoint, 2 * d / 3),
                  last_innpoint)
        inner.reverse()
        for i in range (1, len(inner)):
            start = inner[i-1]
            end = inner[i]
            d = Point.distance(start, end)
            shape.add(Utils.proj(start, end, d / 3), Utils.proj(start, end, 2 * d / 3), end)
        d = Point.distance(end, outer[0])
        shape.add(Utils.proj(end, outer[0], d / 3),
                  Utils.proj(end, outer[0], 2 * d / 3),
                  outer[0])
        return shape

    def linear_brush (self, width: float):
        contour = Brush(self.center).contour_points(self.center, width)
        return self.linear(contour[0], contour[1])

    def rectangles_brush (self, h) -> list[Shape]:
        shapes = []
        pairs = plist(self.center).pairs()
        for pair in pairs:
            shapes.append(Shapes.rect(pair[0], pair[1], h))
        return shapes