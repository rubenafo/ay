import math
import random
import uuid

import cairo
from colour import Color


class Canvas:

    def __init__(self, width=1000, height=1000, seed=random.Random().randint(0,10000)):
        self.seed = seed
        self.rand = random.Random(x=seed)
        self.dim = (width,height)
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.dim[0], self.dim[1])
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgb(1, 1, 1)
        self.context.paint()
        self.context.set_antialias(cairo.ANTIALIAS_BEST)

    def rnd(self):
        return self.rand.random()

    def circle(self, pos, arc, color: Color = Color("black"), alpha: float = 1, strokecolor=None, strokewidth: int = 1):
            self.context.set_line_width(strokewidth)
            if strokecolor:
                self.context.set_source_rgba(strokecolor.get_red(), strokecolor.get_blue(), strokecolor.get_green(), alpha)
                self.context.arc(pos[0], pos[1], arc, 0, 2 * math.pi)
                self.context.stroke_preserve()
                self.context.set_source_rgba(color.get_red(), color.get_blue(), color.get_green(), alpha)
                self.context.fill()
            else:
                self.context.set_source_rgba(color.get_red(), color.get_blue(), color.get_green(), alpha)
                self.context.arc(pos[0], pos[1], arc, 0, 2 * math.pi)
                self.context.stroke()

    def saveToFile(self, filename = uuid.uuid4().hex[:8]):
        print(">> Saving to file: " + '' + str(filename) + '.png ...')
        self.surface.write_to_png('' + str(filename) + '.png')