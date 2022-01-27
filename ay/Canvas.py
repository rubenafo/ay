import math
from numpy import random
import uuid

import skia
from colour import Color

from ay import Shapes
from ay.Gens import Gens
from ay.Point import Point
from ay.Shape import Shape
import ay.utils.Colors
from ay.Layout import Layout


class Canvas ():

    def __init__(self, width=1000, height=1000, seed=random.randint(0,10000),
                 color_seed=random.randint(0,10000)):
        self.seed = seed
        self.surface: skia.Surface = skia.Surface(width, height)
        self.canvas: skia.Canvas = self.surface.getCanvas()
        self.canvas.clear(skia.ColorWHITE)
        self.items: list[Shape] = []
        print (">> using seed: {}".format(self.seed))
        self.rnd = random.default_rng(seed)
        self.color_rnd = random.default_rng(seed)
        self.ft = Gens(self.rnd)
        self.drawn = False
        self.__init_accessors()

    def __init_accessors (self):
        """"
        Set the accessors to use libraries from a canvas instance
        """
        self.colors = ay.utils.Colors
        self.layout = Layout(self.seed)
        self.shapes = Shapes

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
        self.drawn = True

    def with_frame (self, color, width: int):
        Shapes.rect(Point(0, 0), self.surface.width(), width)\
            .fill(color).reg(self)
        Shapes.rect(Point(self.surface.width() - width, 0), width, self.surface.height())\
            .fill(color).reg(self)
        Shapes.rect(Point(0, self.surface.height() - width), self.surface.width(), width)\
            .fill(color).reg(self)
        Shapes.rect(Point(0, 0), width, self.surface.height()).fill(color).reg(self)
        return self

    def save_file(self, filename = uuid.uuid4().hex[:8]):
        filename = filename if ".png" in filename else filename + ".png"
        self.draw() if not self.drawn else None
        print(">> Saving to file: " + '' + str(filename))
        snapshot = self.surface.makeImageSnapshot()
        snapshot.save(filename, skia.kPNG)