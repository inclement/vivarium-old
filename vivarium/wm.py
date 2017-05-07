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
    
# Callbacks

def output_created(handle):
    warning('output_created: {}. Not handled.'.format(handle))
    from vivarium.view import get_output
    get_output(handle)
    return 1

def output_destroyed(handle):
    warning('output_destroyed: {}. Not handled.'.format(handle))

def output_focus(handle, focus):
    warning('output_focus: {}. Not handled.'.format(handle))

def output_resolution(output, from_size, to_size):
    debug('output_resolution: {} from {} -> {}'.format(output, from_size, to_size))
    state.current_workspace.do_layout()

def output_render_pre(handle):
    return
    warning('output_render_pre: {}. Not handle'.format(handle))

def output_render_post(handle):
    return
    warning('output_render_post: {}. Not handle'.format(handle))

def output_context_created(handle):
    warning('output_context_created: {}. Not handle'.format(handle))

def output_context_destroyed(handle):
    warning('output_context_destroyed: {}. Not handle'.format(handle))

def view_created(view):
    debug('view_created: {}'.format(view))

    global state
    state.add_window(view)

    return 1

def view_destroyed(view):
    debug('view_destroyed: {}'.format(view))

    state.destroy_view(view)
    state.current_workspace.do_layout()

def view_focus(view, focus):
    debug('view_focus: {} {}'.format(view, focus))
    wlc.view_set_state(view, lib.WLC_BIT_ACTIVATED, focus)

def view_move_to_output(view, from_output, to_output):
    warning('view_move_to_output: {} from {} -> {}. Not handled.'.format(
        view, from_output, to_output))

def view_request_geometry(view, geometry):
    warning('view_request_geometry. {} requests {}. Not handled.'.format(
        view, geometry))

def view_request_state(view, state, toggle):
    warning('view_request_state: {} requests {}, toggle {}. Not handled.'.format(
        view, state, toggle))

def view_request_move(view, origin):
    warning('view_request_move. Not handled.')

def view_request_resize(view, origin):
    warning('view_request_resize. Not handled.')

def view_render_pre(view):
    return
    warning('view_render_pre. Not handled.')

def view_render_post(view):
    return
    warning('view_render_post. Not handled.')

def view_properties_updated(view, mask):
    warning('view_properties_updated: {} got mask {}. Not handled.'.format(
        view, mask))

def keyboard_key(view, time, modifiers, key, key_state):
    debug('keyboard_key: view {} at {}, modifiers {}, key {}, key_state {}'.format(
        view, time, modifiers, key, key_state))
    return state.keyboard_key(view, time, modifiers, key, key_state)

def pointer_button(view, time, modifiers, button, state, position):
    debug('pointer_button: view {} at {}, modifiers {}, button {}, state {}, position {}'.format(
        view, time, modifiers, button, state, position))
    if state == lib.WLC_BUTTON_STATE_PRESSED:
        wlc.view_focus(view)

    return 0

def pointer_scroll(view, time, modifiers, axis, amount):
    warning('pointer_scroll: view {} at {}, modifiers {}, axis {}, amount ({},  {}, {})'.format(
        view, time, modifiers, axis, amount[0], amount[1], amount[2]))

def pointer_motion(handle, time, position):
    debug('pointer_motion: {} at {} to {}'.format(handle, time, position))
    state.pointer_motion(handle, time, position)

    wlc.pointer_set_position(position)

    return 0

def compositor_ready():
    warning('compositor_ready. Not handled.')

def compositor_terminate():
    warning('compositor_terminate. Not handled.')

def init_callbacks():
    wlc.set_output_created_cb(output_created)
    wlc.set_output_destroyed_cb(output_destroyed)
    wlc.set_output_focus_cb(output_focus)
    wlc.set_output_resolution_cb(output_resolution)
    wlc.set_output_render_pre_cb(output_render_pre)
    wlc.set_output_render_post_cb(output_render_post)
    wlc.set_output_context_created_cb(output_context_created)
    wlc.set_output_context_destroyed_cb(output_context_destroyed)
    wlc.set_view_created_cb(view_created)
    wlc.set_view_destroyed_cb(view_destroyed)
    wlc.set_view_focus_cb(view_focus)
    wlc.set_view_move_to_output_cb(view_move_to_output)
    wlc.set_view_request_geometry_cb(view_request_geometry)
    wlc.set_view_request_state_cb(view_request_state)
    wlc.set_view_request_move_cb(view_request_move)
    wlc.set_view_request_resize_cb(view_request_resize)
    wlc.set_view_render_pre_cb(view_render_pre)
    wlc.set_view_render_post_cb(view_render_post)
    wlc.set_view_properties_updated_cb(view_properties_updated)
    wlc.set_keyboard_key_cb(keyboard_key)
    wlc.set_pointer_button_cb(pointer_button)
    wlc.set_pointer_scroll_cb(pointer_scroll)
    wlc.set_pointer_motion_cb(pointer_motion)
    wlc.set_compositor_ready_cb(compositor_ready)
    wlc.set_compositor_terminate_cb(compositor_terminate)

def init_wlc():
    lib.wlc_init()
    lib.wlc_run()

def run():
    init_callbacks()
    init_wlc()


if __name__ == "__main__":
    run()

