import types

import math

from ay import Point


def resolve(x):
    return x() if isinstance(x, types.FunctionType) else x


def bezier_point(p0: Point, p1: Point, p2: Point, p3: Point, t: float) -> Point:
    t1 = t - 1.0
    x = t * (3 * t1 * (p1.x * t1 - p2.x * t) + p3.x * t * t) - p0.x * t1 * t1 * t1
    y = t * (3 * t1 * (p1.y * t1 - p2.y * t) + p3.y * t * t) - p0.y * t1 * t1 * t1
    return Point.Point(x,y)


def bezier_tangent(a: Point, b: Point, c: Point, d: Point, t: float) -> Point:
    x = 3 * t * t * (-a.x + 3 * b.x - 3 * c.x + d.x) + 6 * t * (a.x - 2 * b.x + c.x) + 3 * (-a.x + b.x)
    y = 3 * t * t * (-a.y + 3 * b.y - 3 * c.y + d.y) + 6 * t * (a.y - 2 * b.y + c.y) + 3 * (-a.y + b.y)
    return Point.Point(x,y)


def proj (p1: Point, p2: Point, di: float) -> Point:
    d = math.sqrt((math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2)))
    r = di / d
    return Point.Point(r * p2.x + (1 - r) * p1.x, r * p2.y + (1 - r) * p1.y)