from colourlovers import clapi


class Colors:

    def palette(self, pid=None):
        cl = clapi.ColourLovers()
        if pid:
            pl = cl.search_palette(id=pid, format='json')
        else:
            pl = cl.search_palettes(request='random', format='json')
        print(">> random palette: {}".format(pl[0].id))
        return list(map(lambda x: '#' + x, pl[0].colors))
