from pywlc import wlc
from vivarium.logger import info, debug, warning, error
from vivarium.layout import TwoColumnLayout, SplittingLayout, RandomLayout


def get_next_workspace_name(identifier, identifiers):
    if identifier is not None:
        return identifier
    i = 1
    while True:
        print(identifiers, str(i), str(i) in identifiers)
        if str(i) not in identifiers:
            return str(i)
        i += 1


class Workspace(object):

    layouts = [TwoColumnLayout(), SplittingLayout()]

    _identifiers = []

    def __init__(self, identifier=None):
        self.identifier = get_next_workspace_name(
            identifier, Workspace._identifiers)
        Workspace._identifiers.append(self.identifier)

        self.windows = []
        self.focused_window = None

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
        self.focused_window = view

        self.do_layout()

    def remove_window(self, view):
        if view not in self.windows:
            return

        if view is self.focused_window:
            self.up()

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
                    self.focused_window = window
                    return True

    def focus(self):
        if not self.windows:
            return
        if self.focused_window is not None:
            self.focused_window.focus()

    def left(self):
        self.current_layout.left()
        self.do_layout()

    def right(self):
        self.current_layout.right()
        self.do_layout()

    def up(self):
        index = self.windows.index(self.focused_window)
        self.focused_window = self.windows[(index - 1) % len(self.windows)]
        self.focused_window.focus()

    def down(self):
        index = self.windows.index(self.focused_window)
        self.focused_window = self.windows[(index + 1) % len(self.windows)]
        self.focused_window.focus()
