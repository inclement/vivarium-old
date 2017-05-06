
from pywlc import wlc
from vivarium.logger import info, debug, warning, error


views = {}
def get_view(handle):
    if handle not in views:
        views[handle] = View(handle)
        handles[handle] = views[handle]
    return views[handle]

outputs = {}
def get_output(handle):
    if handle not in outputs:
        outputs[handle] = Output(handle)
        handles[handle] = outputs[handle]
    return outputs[handle]

handles = {}
def get_handle(handle):
    return handles[handle]

class WlcHandle(object):
    def __init__(self, handle=None):
        if handle is None:
            raise ValueError('wlc handle must not be None')
        self.handle = handle


class View(WlcHandle):

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self._size = (800, 600)
        self._pos = (0, 0)

        self.visible = True

        wlc.view_set_mask(self.handle,
                          wlc.output_get_mask(wlc.view_get_output(self.handle)))


    @property
    def output(self):
        return Output(wlc.view_get_output(self.handle))

    def bring_to_front(self):
        wlc.view_bring_to_front(self.handle)

    def focus(self):
        wlc.view_focus(self.handle)

    def set(self, size=None, pos=None):
        g = wlc.WlcGeometry()
        debug('asked to set size {} pos {}'.format(size, pos))
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


        wlc.view_set_geometry(self.handle, 0, g)

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


class Output(WlcHandle):

    @property
    def virtual_resolution(self):
        return wlc.output_get_virtual_resolution(self.handle)

