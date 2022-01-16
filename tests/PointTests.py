import unittest

from ay.Point import Point


class PointTests (unittest.TestCase):

    def test_tang (self):
        p0 = Point(0,0)
        p1 = Point (20,20)
        tang = Point.tang(p0, p0, p1, p1, 0.5)
        print(tang)

    def test_angle (self):
        a = Point.angle(Point(100,100), Point(50,50))
        self.assertEqual(a, 45.0)

    def test_point_at (self):
        p = Point.point_at(Point(0,0), Point(0,0), Point(100,100), Point(100,100), 0.5)
        self.assertEqual(Point(50,50), p)
        p = Point.point_at(Point(100,100), Point(100,100), Point(1000,100), Point(1000,100), 0.2)
        self.assertEqual(Point(193.6, 100), p)