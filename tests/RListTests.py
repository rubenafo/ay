import unittest

from ay.Point import Point
from ay.plist import plist


class PListTests(unittest.TestCase):

    def test_interpolate (self):
        mylist = plist([Point(0, 0), Point(20, 30)])
        points = mylist.interpolate()
        self.assertEqual(3, len(points))
        self.assertEqual(Point(10, 15), points[1])
