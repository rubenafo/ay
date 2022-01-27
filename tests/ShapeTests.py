
import unittest

from ay.Point import Point
from ay.Shape import Shape
from ay import Shapes


class ShapeTests (unittest.TestCase):

    def test_rect_from_point_width_height (self):
        rect = Shapes.rect(Point(100,100), 300, 300)
        self.assertEqual(4, len(rect.segments))
        self.assertEqual(Point(100,100), rect.head)
        self.assertEqual(Point(400,100), rect.segments[0]['p2'])
        self.assertEqual(Point(400,400), rect.segments[1]['p2'])
        self.assertEqual(Point(100,400), rect.segments[2]['p2'])

    def test_rect_from_two_points (self):
        rect = Shapes.rect(Point(100, 100), Point(100, 400), 20)
        self.assertEqual(4, len(rect.segments))

    def test_subd(self):
        rect = Shapes.rect(Point(100, 100), 300, 300)
        rect.subd(0.5)
        self.assertEqual(8, len(rect.segments))
        self.assertEqual(Point(100, 100), rect.head)
        self.assertEqual(Point(250, 100), rect.segments[0]['p2'])
        self.assertEqual(Point(400, 100), rect.segments[1]['p2'])
        self.assertEqual(Point(400, 250), rect.segments[2]['p2'])
        self.assertEqual(Point(400, 400), rect.segments[3]['p2'])
        self.assertEqual(Point(250, 400), rect.segments[4]['p2'])
        self.assertEqual(Point(100, 400), rect.segments[5]['p2'])
        self.assertEqual(Point(100, 250), rect.segments[6]['p2'])
        self.assertEqual(Point(100, 100), rect.segments[7]['p2'])
