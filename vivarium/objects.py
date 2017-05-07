from __future__ import division
from pywlc import wlc
from vivarium.logger import info, debug, warning, error
from vivarium.workspace import Workspace
from vivarium.view import (View, Output, get_view, get_output,
                           get_handle)
from vivarium import functions



keyboard_shortcuts = [('ctrl', 'Escape', functions.quit),
                      ('ctrl', 'Return', functions.spawn('xterm')),
                      ('ctrl', 'space', functions.next_layout),
                      ('ctrl', 'h', functions.left),
                      ('ctrl', 'l', functions.right),
                      ('ctrl', 'j', functions.down),
                      ('ctrl', 'k', functions.up),
                      ]

for i in range(1, 10):
    keyboard_shortcuts.append(
        ('ctrl', str(i), functions.to_workspace(str(i)))
        )

class State(object):

    workspaces = []

    keyboard_shortcuts = keyboard_shortcuts

    # Miscellaneous settings options:
    layout_step = 0.04

    def __init__(self):
        self.workspaces = [Workspace(), Workspace()]
        self.current_workspace = self.workspaces[0]


    def add_window(self, view):
        view = get_view(view)

        parent = wlc.view_get_parent(view.handle)
        debug('parent is {}'.format(parent))

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

        for shortcut in keyboard_shortcuts:
            modifier, key, func = shortcut
            if modifiers.modifiers == [modifier]:
                if sym == wlc.keysym(key):
                    func()
                    return 1

        return 0

    def next_layout(self):
        self.current_workspace.next_layout()

    def quit(self):
        wlc.terminate()


    def left(self):
        debug('state.left')
        self.current_workspace.left()
        return 1

    def right(self):
        debug('state.right')
        self.current_workspace.right()
        return 1
        
    def up(self):
        debug('state.up')
        self.current_workspace.up()
        return 1

    def down(self):
        debug('state.down')
        self.current_workspace.down()
        return 1

    def to_workspace(self, identifier):
        debug('state.to_workspace {}: options are {}'.format(
            identifier, [w.identifier for w in self.workspaces]))
        matching = [w for w in self.workspaces if w.identifier == identifier]
        if not matching:
            error('Could not switch to workspace "{}", it does not '
                  'exist'.format(identifier))
        self.current_workspace = matching[0]
        self.current_workspace.focus()
        

import os
os.environ['XKB_DEFAULT_LAYOUT'] = 'gb'
os.environ['XKB_DEFAULT_VARIANT'] = 'widecolemak'

state = State()
