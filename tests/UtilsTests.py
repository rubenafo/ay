import unittest

from ay.Point import Point


class UtilsTests(unittest.TestCase):

    def test_proj(self):
        mid = Point.mid(Point(100,100), Point(200,200))
        self.assertEqual(Point(150,150), mid)