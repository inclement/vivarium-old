from pywlc import wlc


class Layout(object):

    def __init__(self):
        self.tiled_windows = []
        self.floating_windows = []

    @property
    def windows(self):
        return self.tiled_windows + self.floating_windows

    def add_window(self, window):
        window.bring_to_front()
        window.focus()

        size = window.output.virtual_resolution
        print('adding window to output with size {}'.format(size))

        from random import randint
        window.set(pos=(randint(0, size.w - 800), randint(0, size.h - 600)))
        


class TwoColumnLayout(Layout):
    pass

class RandomLayout(Layout):
    pass


class Output(object):
    def __init__(self, index):
        self.index = index

    @property
    def virtual_resolution(self):
        return wlc.output_get_virtual_resolution(self.index)

class View(object):

    def __init__(self, index):
        self.index = index

        self.size = (800, 600)
        self.pos = (0, 0)

        wlc.view_set_mask(index, wlc.output_get_mask(wlc.view_get_output(index)))


    @property
    def output(self):
        return Output(wlc.view_get_output(self.index))

    def bring_to_front(self):
        wlc.view_bring_to_front(self.index)

    def focus(self):
        wlc.view_focus(self.index)

    def set(self, size=None, pos=None):
        g = wlc.WlcGeometry()
        print('asked to set', size, pos)
        if size is not None:
            g.size.w = size[0]
            g.size.h = size[1]
        else:
            g.size.w = self.size[0]
            g.size.h = self.size[1]

        if pos is not None:
            g.origin.x = pos[0]
            g.origin.y = pos[1]
        else:
            g.origin.x = self.pos[0]
            g.origin.y = self.pos[1]

        print('Setting geometry to', g)
        wlc.view_set_geometry(self.index, 0, g)


class State(object):
    layouts = [TwoColumnLayout()]

    def __init__(self):
        self.current_layout = self.layouts[0]


    def add_window(self, view):
        view = View(view)

        self.current_layout.add_window(view)
