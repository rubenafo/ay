
import unittest

from ay.Point import Point
from ay.Shape import Shape


class ShapeTests (unittest.TestCase):

    def test_rect (self):
        rect = Shape.rect(100, 100, 300, 300)
        self.assertEqual(13, len(rect.pxs))
        self.assertEqual((100,100), (rect.pxs[0], rect.pys[0]))
        self.assertEqual((400,100), (rect.pxs[3], rect.pys[3]))
        self.assertEqual((400,400), (rect.pxs[6], rect.pys[6]))
        self.assertEqual((100,400), (rect.pxs[9], rect.pys[9]))

    def test_subd(self):
        rect = Shape.rect(100, 100, 300, 300)
        rect.subd(0.5)
        self.assertEqual(25, len(rect.pxs))
