import unittest

from ay.Point import Point
from ay.plist import plist


class PListTests (unittest.TestCase):

    def test_closest(self):
        pts = plist([Point(0,0), Point(100,100), Point(50,50), Point(-50,60)])
        self.assertEqual(Point(0,0), pts.closest(Point(20,20)))
        self.assertEqual(Point(100,100), pts.closest(Point(110,100)))
        self.assertEqual(Point(-50, 60), pts.closest(Point(-60, 40)))
        self.assertEqual(Point(100,100), pts.closest(Point(0,0)))

    def test_furthest (self):
        pts = plist([Point(0,0), Point(100,100), Point(50,50), Point(-50,60)])
        self.assertEqual(Point(100,100), pts.furthest(Point(20,20)))
        self.assertEqual(Point(100,100), pts.furthest(Point(-50,60)))
        self.assertEqual(Point(-50,60), pts.furthest(Point(200,200)))

    def test_pairs(self):
        pts = plist([Point(0,0), Point(100,100), Point(50,50), Point(-50,60)])
        pairs = pts.pairs()
        self.assertEqual(3, len(pairs))

    def test_chunks (self):
        pts = plist([Point(0,0), Point(100,100),
                     Point(50,50), Point(-50,60),
                     Point(1,1), Point(-6,6)])
        chunks = pts.chunks(2)
        self.assertEqual(3, len(chunks))
        chunks = pts.chunks(3)
        self.assertEqual(2, len(chunks))

    def test_chunks_with_overlap (self):
        pts = plist([Point(0, 0), Point(100, 100),
                     Point(50, 50), Point(-50, 60),
                     Point(1, 1), Point(-6, 6)])
        chunks = pts.chunks(3,1)
        self.assertEqual(2, len(chunks))