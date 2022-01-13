import math
import random
import uuid

import skia
from colour import Color

from ay.Point import Point
from ay.Shape import Shape


class Canvas:

    def __init__(self, width=1000, height=1000, seed=random.Random().randint(0,10000)):
        self.seed = seed
        self.rand = random.Random(x=seed)
        self.surface: skia.Surface = skia.Surface(width, height)
        self.canvas: skia.Canvas = self.surface.getCanvas()
        self.canvas.clear(skia.ColorWHITE)
        self.items: list[Shape] = []

    def rnd(self):
        return self.rand.random()

    def rpoint (self, a, b):
        return Point(self.rnd()*a, self.rnd()*b)

    def add (self, s: Shape):
        self.items.append(s)
        return self

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

    def draw(self):
        for i in self.items:
            if 'fill' in i.style:
                paint = skia.Paint()
                paint.setStyle(skia.Paint.kFill_Style)
                paint.setAntiAlias(True)
                paint.setColor(i.style['fill'])
                self.canvas.drawPath(i.draw(), paint)
            if 'stroke' in i.style:
                paint = skia.Paint()
                paint.setStyle(skia.Paint.kStroke_Style)
                paint.setStrokeWidth(i.style['stroke_width'])
                paint.setColor(i.style['stroke'])
                paint.setAntiAlias(True)
                self.canvas.drawPath(i.draw(), paint)

    def save_file(self, filename = uuid.uuid4().hex[:8]):
        print(">> Saving to file: " + '' + str(filename) + '.png ...')
        snapshot = self.surface.makeImageSnapshot()
        snapshot.save(filename + ".png", skia.kPNG)