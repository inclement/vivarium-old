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

        self.tiled_windows.append(window)

        self.do_layout()

    def remove_window(self, index):
        if not any(w.index == index for w in self.windows):
            return

        for i, window in enumerate(self.tiled_windows):
            if window.index == index:
                self.tiled_windows.pop(i)

                if self.tiled_windows:
                    self.tiled_windows[max(i - 1, 0)].focus()

        for i, window in enumerate(self.floating_windows):
            if window.index == index:
                self.floating_windows.pop(i)

                if self.floating_windows:
                    self.floating_windows[max(i - 1, 0)].focus()
        
        self.do_layout()

    def do_layout(self):
        pass
        


class TwoColumnLayout(Layout):

    def __init__(self):
        super(TwoColumnLayout, self).__init__()
        self.separator_frac = 0.6667

    def do_layout(self):

        width_frac = self.separator_frac if len(self.tiled_windows) > 1 else 1

        window = self.tiled_windows[0]
        output_size = window.output.virtual_resolution
        output_size = (output_size.w, output_size.h)
        
        window.set(pos=(0, 0),
                   size=(int(width_frac * output_size[0]),
                           output_size[1]))

        if len(self.tiled_windows) <= 1:
            return
        height = output_size[1] / (len(self.tiled_windows) - 1)
        width = (1 - width_frac) * output_size[0]
        for i, window in enumerate(self.tiled_windows[1:]):
            window.size = (int(width), int(height))
            window.pos = (int(output_size[0] * width_frac),
                          int(output_size[1] - height * (1 + i)))


class RandomLayout(Layout):
    def do_layout(self):
        from random import randint

        for window in self.tiled_windows:
            size = window.output.virtual_resolution
            window.set(pos=(randint(0, size.w - 800), randint(0, size.h - 600)))



class Output(object):
    def __init__(self, index):
        self.index = index

    @property
    def virtual_resolution(self):
        return wlc.output_get_virtual_resolution(self.index)

class View(object):

    def __init__(self, index):
        self.index = index

        self._size = (800, 600)
        self._pos = (0, 0)

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
            self._size = size
        else:
            g.size.w = self.size[0]
            g.size.h = self.size[1]

        if pos is not None:
            g.origin.x = pos[0]
            g.origin.y = pos[1]
            self._pos = pos
        else:
            g.origin.x = self.pos[0]
            g.origin.y = self.pos[1]


        print('Setting geometry to', g)
        wlc.view_set_geometry(self.index, 0, g)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self.set(size=value)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self.set(pos=value)


class State(object):
    layouts = [TwoColumnLayout()]

    def __init__(self):
        self.current_layout = self.layouts[0]


    def add_window(self, view):
        view = View(view)

        self.current_layout.add_window(view)

    def destroy_view(self, view):
        for layout in self.layouts:
            layout.remove_window(view)
                    
