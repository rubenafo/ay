from colourlovers import clapi
import colour

from ay.plist import plist


def palette(pid=None):
    cl = clapi.ColourLovers()
    if pid:
        pl = cl.search_palette(id=pid, format='json')
    else:
        pl = cl.search_palettes(request='random', format='json')
    print(">> random palette: {}".format(pl[0].id))
    return plist(map(lambda x: '#' + x, pl[0].colors))


def color(hex1:str, hex2:str, steps: int) -> list[str]:
    return list(map(lambda x: x.hex, list(colour.Color(hex1).range_to(colour.Color(hex2), steps))))


def color(hex1:str, hex2:str, hex3:str, steps:int) -> list[str]:
    range1 = color(hex1, hex2, steps)
    range2 = color(hex2, hex3, steps)
    return range1 + range2

