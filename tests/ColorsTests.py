
import unittest

import colour

from ay.utils import Colors


class ColorsTests (unittest.TestCase):

    def test_range_colors (self):
        color_range = Colors.color("#000000", "#00aabb", 10)
        self.assertEqual(10, len(color_range))
        self.assertEqual(colour.Color("black").hex, color_range[0])
        self.assertEqual(colour.Color("#00aabb").hex, color_range[9])

