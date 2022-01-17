import unittest

from ay.Point import Point
from ay.rlist import rlist


class RListTests(unittest.TestCase):

    def test_interpolate (self):
        mylist = rlist([Point(0,0), Point(20, 30)])
        points = mylist.interpolate()
        self.assertEqual(3, len(points))
        self.assertEquals(Point(10, 15), points[1])
