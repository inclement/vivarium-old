from __future__ import division, print_function
from pywlc import ffi, lib
from pywlc import wlc

from vivarium.objects import state
from vivarium.logger import logger, info, debug, warning, error
import logging
logger.setLevel(logging.DEBUG)

from colorama import Fore, Style

import random

info('{Fore.GREEN}{Style.BRIGHT}Running vivarium{Fore.RESET}'.format(Fore=Fore, Style=Style))

def get_topmost(output, offset):
    views, num_views = wlc.output_get_views(output)
    if num_views > 0:
        return views[(num_views - 1 + offset) % num_views]
    return 0

def do_layout(output):
    size = wlc.output_get_virtual_resolution(output)
    
    views, num_views = wlc.output_get_views(output)

    positioned = 0
    for i in range(num_views):
        if wlc.view_positioner_get_anchor_rect(views[i]) == wlc.NULL:
            positioned += 1

    toggle = 0
    y = 0
    n = max((1 + positioned) // 2, 1)
    w = size.w // 2
    h = size.h // n
    ew = size.w - w * 2
    eh = size.h - h * n
    j = 0

    for i in range(num_views):
        anchor_rect = wlc.view_positioner_get_anchor_rect(views[i])
        if anchor_rect == wlc.NULL:
            g = wlc.WlcGeometry()
            g.origin.x = w + ew if toggle else 0
            g.origin.y = y
            g.size.w = (
                size.w if ((1 - toggle) and j == positioned - 1)
                else (w if toggle else w + ew))
            g.size.h = h + eh if j < 2 else h

            wlc.view_set_geometry(views[i], 0, g)

            toggle = 1 - toggle
            y = y + (g.size.h if not toggle else 0)
            j += 1

        else:
            size_req = wlc.view_positioner_get_size(views[i])
            if size_req.w <= 0 or size_req.h <= 0:
                current = wlc.view_get_geometry(views[i])
                size_req = current.size

            g = wlc.WlcGeometry()
            g.origin = anchor_rect.origin
            g.size = size_req

            parent = wlc.view_get_parent(views[i])

            if parent:
                parent.geometry = wlc.view_get_geometry(parent)
                g.origin.x += parent_geometry.origin.x
                g.origin.y += parent_geometry.origin.y

            wlc.view_set_geometry(views[i], 0, g)
    

def output_resolution(output, from_size, to_size):
    state.current_workspace.do_layout()

def output_created(handle):
    debug('Output created: {}'.format(handle))
    from vivarium.view import get_output
    get_output(handle)
    return 1
    
def view_created(view):

    global state
    state.add_window(view)

    # wlc.view_set_mask(view, wlc.output_get_mask(wlc.view_get_output(view)))
    # wlc.view_bring_to_front(view)
    # wlc.view_focus(view)

    # do_layout(wlc.view_get_output(view))

    return 1

def view_destroyed(view):

    # wlc.view_focus(get_topmost(wlc.view_get_output(view), 0))
    state.destroy_view(view)
    state.current_workspace.do_layout()
    # do_layout(wlc.view_get_output(view))

def view_focus(view, focus):
    wlc.view_set_state(view, lib.WLC_BIT_ACTIVATED, focus)

def view_request_move(view, origin):
    pass

def view_request_resize(view, origin):
    pass

def view_request_geometry(view, geometry):
    pass

def keyboard_key(view, time, modifiers, key, key_state):

    return state.keyboard_key(view, time, modifiers, key, key_state)

    sym = wlc.keyboard_get_keysym_for_key(key)

    if view:
        if 'ctrl' in modifiers:
            if sym == wlc.keysym('q'):
                if state:
                    wlc.view_close(view)

    if 'ctrl' in modifiers:
        if sym == wlc.keysym('Escape'):
            if state:
                wlc.terminate()
            return 1

        if sym == wlc.keysym('Return'):
            if state:
                wlc.exec('weston-terminal')
            return 1

    return 0

def pointer_button(view, time, modifiers, button, state, position):

    if state == lib.WLC_BUTTON_STATE_PRESSED:
        wlc.view_focus(view)

    return 0


def pointer_motion(handle, time, position):

    state.pointer_motion(handle, time, position)

    wlc.pointer_set_position(position)

    return 0

def init_callbacks():
    wlc.set_output_resolution_cb(output_resolution)
    wlc.set_output_created_cb(output_created)
    wlc.set_view_created_cb(view_created)
    wlc.set_view_destroyed_cb(view_destroyed)
    wlc.set_view_focus_cb(view_focus)
    wlc.set_view_request_move_cb(view_request_move)
    wlc.set_view_request_resize_cb(view_request_resize)
    wlc.set_view_request_geometry_cb(view_request_geometry)
    wlc.set_keyboard_key_cb(keyboard_key)
    wlc.set_pointer_button_cb(pointer_button)
    wlc.set_pointer_motion_cb(pointer_motion)

def init_wlc():
    lib.wlc_init()
    lib.wlc_run()

def run():
    init_callbacks()
    init_wlc()


if __name__ == "__main__":
    run()

