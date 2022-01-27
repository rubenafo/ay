import unittest

from ay.Point import Point
from ay.utils.Brush import Brush


class BrushTest(unittest.TestCase):

    def test_contour_points (self):
        br = Brush([Point(100, 100), Point(500, 100), Point (500,200)])
        ct = br.contour_points([Point(100, 100), Point(500, 100), Point (500,200)], 30)
        self.assertEqual([Point(100,90), Point(500,90)], ct[0])
        self.assertEqual([Point(100,110), Point(500,110)], ct[1])
        shape = br.linear(ct[0], ct[1])
        self.assertEqual(13, len(shape.pxs))
        self.assertEqual(13, len(shape.pys))

