from pywlc import wlc


def get_state():
    from vivarium.objects import state
    return state


def spawn(program):
    def func():
        wlc.exec(program)
    return func


def next_layout():
    state = get_state()
    state.next_layout()

def left():
    state = get_state()
    state.left()

def right():
    state = get_state()
    state.left()
    
