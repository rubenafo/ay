from ay.Point import Point
from ay import Shape
from ay.plist import plist
from ay.utils import Spline


def rect(p0: Point, *args):
    """
    rect (Point, width, height)
    rect (Point, Point, width)
    """
    assert len(args) == 2 or len(args) == 1
    param1 = args[0]
    param2 = args[1]
    if type(param1) == Point:
        assert type(param2) == int or type(param2) == float
        p1, height = args
        dist = Point.distance(p0, p1)
        angle = Point.angle(p0, p1)
        return rect(Point(p0.x, p0.y - height/2), dist, height)\
            .rotate(angle, p0)
    else:
        width, height = args
        p1 = Point (p0.x+width, p0.y)
        p2 = Point (p1.x, p1.y + height)
        p3 = Point (p0.x, p0.y + height)
        return Shape.Shape.line(p0, p1).addPoint(p2).addPoint(p3).addPoint(p0)


def curve(p0: Point, p1: Point, p2: Point, p3: Point) -> Shape:
    s = Shape.Shape()
    p0 = p0 if type(p0) == Point else Point(p0[0], p0[1])
    c1 = p1 if type(p1) == Point else Point(p1[0], p1[1])
    c2 = p2 if type(p2) == Point else Point(p2[0], p2[1])
    p2 = p3 if type(p3) == Point else Point(p3[0], p3[1])
    s.head = p0
    s.add(c2, c1, p2)
    s.closed = False
    return s


def circle(p: Point, r: float) -> Shape:
    c = 0.551915024494 * r
    circle = Shape.Shape(Point(0, -r))
    circle.add(Point(-c, -r), Point(-r, -c), Point(-r, 0))
    circle.add(Point(-r, c), Point(-c, r), Point(0, r))
    circle.add(Point(c, r), Point(r, c), Point(r, 0))
    circle.add(Point(r, -c), Point(c, -r), Point(0, -r))
    return circle.translate(p)


def triangle (p0: Point, p1: Point, p2: Point):
    return Shape.Shape(p0).addPoint(p1).addPoint(p2)


def spline(pts: list, numpoints: float = 100) -> plist:
    ps = Spline.bspline(pts.as_tuples(), numpoints, 4)
    return plist([Point(p[0], p[1]) for p in ps])