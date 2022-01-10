import math
import random
import uuid

import pixie
from colour import Color

from ay.Point import Point
from ay.Shape import Shape


class Canvas:

    def __init__(self, width=1000, height=1000, seed=random.Random().randint(0,10000)):
        self.seed = seed
        self.rand = random.Random(x=seed)
        self.canvas: pixie.Image = pixie.Image(width, height)
        self.canvas.fill(pixie.parse_color("#FFFFFF"))
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
            paint = pixie.Paint(pixie.PK_SOLID)
            paint.color = pixie.Color(255, 45, 6, 0.2)

            #st = pixie.Paint(pixie.PK_SOLID)
            #st.color = pixie.parse_color("#FF5C00")

            ctx: pixie.Context = self.canvas.new_context()
            ctx.stroke_style = paint
            ctx.line_width = 10
            ctx.path_stroke(i.draw())

            #self.canvas.fill_path(i.draw(), st)

            #self.canvas.stroke_path(i.draw(), paint)


    def saveToFile(self, filename = uuid.uuid4().hex[:8]):
        print(">> Saving to file: " + '' + str(filename) + '.png ...')
        self.canvas.write_file(filename + ".png")