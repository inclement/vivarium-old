
from pywlc import wlc
from vivarium.logger import info, debug, warning, error

class Layout(object):

    def __init__(self):

        self.border = 1

    def do_layout(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

class TwoColumnLayout(Layout):

    def __init__(self):
        super(TwoColumnLayout, self).__init__()
        self.separator_frac = 0.6667

    def do_layout(self, windows):

        debug('TwoColumnLayout.do_layout: {} windows'.format(len(windows)))

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

    def left(self):
        self.separator_frac -= state.layout_step
        debug('left: {}.separator_frac = {}'.format(self, self.separator_frac))
        self.separator_frac = max(0, self.separator_frac)

    def right(self):
        self.separator_frac += state.layout_step
        debug('right: {}.separator_frac = {}'.format(self, self.separator_frac))
        self.separator_frac = min(1, self.separator_frac)


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
