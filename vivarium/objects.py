from __future__ import division
from pywlc import wlc
from vivarium.logger import info, debug, warning
from vivarium import functions

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


def get_next_workspace_name(identifier, identifiers):
    if identifier is not None:
        return identifier
    i = 1
    while True:
        if str(i) not in identifiers:
            return str(i)
        i += 1



class Layout(object):

    def __init__(self):

        self.border = 1

    def do_layout(self):
        pass


class TwoColumnLayout(Layout):

    def __init__(self):
        super(TwoColumnLayout, self).__init__()
        self.separator_frac = 0.6667

    def do_layout(self, windows):

        debug('TwoColumnLayout do_layout called')

        width_frac = self.separator_frac if len(windows) > 1 else 1

        if not windows:
            return

        window = windows[0]
        output_size = window.output.virtual_resolution
        output_size = (output_size.w, output_size.h)

        debug('output_size is {}'.format(output_size))
        
        window.set(pos=(self.border, self.border),
                   size=(int(width_frac * output_size[0] - 2*self.border),
                           output_size[1] - 2*self.border))

        if len(windows) <= 1:
            return
        height = output_size[1] / (len(windows) - 1)
        width = (1 - width_frac) * output_size[0]
        debug('width is {}, height is {}'.format(width, height))
        for i, window in enumerate(windows[1:]):
            size = (int(width - 2*self.border), int(height - 2*self.border))
            if size[0] < 0:
                error('Tried to set window width to {}'.format(size[0]))
                continue
            if size[1] < 0:
                error('Tried to set window height to {}'.format(size[1]))
                continue
            pos = (int(output_size[0] * width_frac + self.border),
                   int(height * i + self.border))
            window.set(size=size,
                       pos=pos)


class SplittingLayout(Layout):
    def do_layout(self, windows):

        window = windows[0]
        output_size = window.output.virtual_resolution
        output_size = (output_size.w, output_size.h)

        current_width = output_size[0]
        current_height = output_size[1]
        current_x = 0
        current_y = 0
        dir = 'horizontal'
        while windows:
            window = windows[0]
            windows = windows[1:]

            if not windows:
                window.set(size=(current_width - 2*self.border,
                                 current_height - 2*self.border),
                           pos=(current_x + self.border,
                                current_y + self.border))
                continue

            if dir == 'horizontal':
                current_width = int(current_width / 2.)
            else:
                current_height = int(current_height / 2.)

            window.set(size=(current_width - 2*self.border,
                             current_height - 2*self.border),
                       pos=(current_x + self.border,
                            current_y + self.border))

            if dir == 'horizontal':
                current_x = current_x + current_width
                dir = 'vertical'
            else:
                current_y = current_y + current_height
                dir = 'horizontal'



class RandomLayout(Layout):
    def do_layout(self, windows):
        from random import randint

        for window in windows:
            size = window.output.virtual_resolution
            window.set(pos=(randint(0, size.w - 800), randint(0, size.h - 600)))



class Output(WlcHandle):

    @property
    def virtual_resolution(self):
        return wlc.output_get_virtual_resolution(self.handle)

class View(WlcHandle):

    def __init__(self, *args, **kwargs):
        print('args are', args, kwargs)
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


        print('Setting geometry to', g)
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


class Workspace(object):

    layouts = [TwoColumnLayout(), SplittingLayout()]

    _identifiers = []

    def __init__(self, identifier=None):
        self.identifier = get_next_workspace_name(
            identifier, Workspace._identifiers)

        self.windows = []

    @property
    def current_layout(self):
        return self.layouts[0]

    def next_layout(self):
        self.layouts = self.layouts[1:] + [self.layouts[0]]
        self.do_layout()

    def do_layout(self):
        self.current_layout.do_layout(self.windows)

    def add_window(self, view):
        view.bring_to_front()
        view.focus()
        self.windows.append(view)

        self.do_layout()


    def remove_window(self, view):
        if view not in self.windows:
            return

        index = self.windows.index(view)
        self.windows.pop(index)
        if self.windows:
            self.windows[max(index - 1, 0)].focus()

        self.do_layout()

    def pointer_motion(self, handle, time, position):
        for window in self.windows[::-1]:
            pos = window.pos
            size = window.size
            if pos[0] < position.x < pos[0] + size[0]:
                if pos[1] < position.y < pos[1] + size[1]:
                    window.focus()
                    return True


keyboard_shortcuts = [('ctrl', 'Escape', 'quit'),
                      ('ctrl', 'Return', functions.spawn('xterm')),
                      ('ctrl', 'space', functions.next_layout),
                      ]

class State(object):

    workspaces = []

    keyboard_shortcuts = keyboard_shortcuts

    def __init__(self):
        self.workspaces = [Workspace(), Workspace()]
        self.current_workspace = self.workspaces[0]


    def add_window(self, view):
        view = get_view(view)

        self.current_workspace.add_window(view)

    def destroy_view(self, view):
        view = get_view(view)
        for workspace in self.workspaces:
            workspace.remove_window(view)

    def pointer_motion(self, handle, time, position):
        for workspace in self.workspaces:
            if workspace.pointer_motion(handle, time, position):
                return

    def keyboard_key(self, view, time, modifiers, key, key_state):
        sym = wlc.keyboard_get_keysym_for_key(key)

        if not key_state:
            return 0

        if modifiers.modifiers == ['ctrl'] and sym == wlc.keysym('i'):
            print('view is {}, current mask is {}'.format(
                view, wlc.view_get_mask(view)))
            wlc.view_set_mask(view, 1 - wlc.view_get_mask(view))

        for shortcut in keyboard_shortcuts:
            modifier, key, func = shortcut
            if modifiers.modifiers == [modifier]:
                if sym == wlc.keysym(key):
                    if isinstance(func, str):
                        return getattr(self, func)()
                    else:
                        return func()

        return 0

    def next_layout(self):
        self.current_workspace.next_layout()

    def quit(self):
        wlc.terminate()
        

state = State()
