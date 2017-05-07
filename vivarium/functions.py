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
    return 1

def left():
    state = get_state()
    state.left()
    return 1

def right():
    state = get_state()
    state.right()
    return 1
    
def up():
    state = get_state()
    state.up()
    return 1

def down():
    state = get_state()
    state.down()
    return 1

def to_workspace(identifier):
    def func():
        state = get_state()
        state.to_workspace(identifier)
        return 1
    return func

def quit():
    state = get_state()
    state.quit()
    return 1

def close_window():
    state = get_state()
    state.close_window()
