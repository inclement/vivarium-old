from pywlc import ffi, lib
from pywlc import wlc
# from pywm.callbacks import lib, ffi
    
def output_resolution(output, from_size, to_size):
    print('output resolution', output, from_size, to_size)
    
def view_created(view):
    print('view_created')

def view_destroyed(view):
    print('view_destroyed')

def view_focus(view):
    print('view_focus')

def view_request_move(view):
    print('view_request_move')

def view_request_resize(view):
    print('view_request_resize')

def keyboard_key(view, time, modifiers, key, state):
    print('keyboard_key', view, time, modifiers, key, state)

    sym = wlc.keyboard_get_keysym_for_key(key)

    if 'ctrl' in modifiers:
        if sym == wlc.keysym('Escape'):
            if state:
                wlc.terminate()
            return 1

    return 0

def pointer_button(view):
    print('pointer_button')

def pointer_motion(handle, time, position):
    # print('pointer_motion', handle, time, position)

    wlc.pointer_set_position(position)

    return 0

def init_callbacks():
    wlc.set_output_resolution_cb(output_resolution)
    wlc.set_view_created_cb(view_created)
    wlc.set_view_destroyed_cb(view_destroyed)
    wlc.set_view_focus_cb(view_focus)
    wlc.set_view_request_move_cb(view_request_move)
    wlc.set_view_request_resize_cb(view_request_resize)
    wlc.set_keyboard_key_cb(keyboard_key)
    wlc.set_pointer_button_cb(pointer_button)
    wlc.set_pointer_motion_cb(pointer_motion)

def run():
    init_callbacks()

    lib.wlc_init()
    lib.wlc_run()


if __name__ == "__main__":
    run()

