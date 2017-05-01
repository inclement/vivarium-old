import logging
from sys import stdout, stderr
from colorama import Style as Colo_Style, Fore as Colo_Fore
from collections import defaultdict

class LevelDifferentiatingFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno > 30:
            record.msg = '{}{}[ERROR]{}{}:   '.format(
                Err_Style.BRIGHT, Err_Fore.RED, Err_Fore.RESET,
                Err_Style.RESET_ALL) + record.msg
        elif record.levelno > 20:
            record.msg = '{}{}[WARNING]{}{}: '.format(
                Err_Style.BRIGHT, Err_Fore.RED, Err_Fore.RESET,
                Err_Style.RESET_ALL) + record.msg
        elif record.levelno > 10:
            record.msg = '{}[INFO]{}:    '.format(
                Err_Style.BRIGHT, Err_Style.RESET_ALL) + record.msg
        else:
            record.msg = '{}{}[DEBUG]{}{}:   '.format(
                Err_Style.BRIGHT, Err_Fore.LIGHTBLACK_EX, Err_Fore.RESET,
                Err_Style.RESET_ALL) + record.msg
        return super(LevelDifferentiatingFormatter, self).format(record)

logger = logging.getLogger('p4a')

if not hasattr(logger, 'touched'):  # Necessary as importlib reloads
                                    # this, which would add a second
                                    # handler and reset the level
    logger.setLevel(logging.INFO)
    logger.touched = True
    ch = logging.StreamHandler(stderr)
    formatter = LevelDifferentiatingFormatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error

    
class colorama_shim(object):

    def __init__(self, real):
        self._dict = defaultdict(str)
        self._real = real
        self._enabled = False

    def __getattr__(self, key):
        return getattr(self._real, key) if self._enabled else self._dict[key]

    def enable(self, enable):
        self._enabled = enable

Out_Style = colorama_shim(Colo_Style)
Out_Fore = colorama_shim(Colo_Fore)
Err_Style = colorama_shim(Colo_Style)
Err_Fore = colorama_shim(Colo_Fore)


def setup_color(color):
    enable_out = (False if color == 'never' else
                  True if color == 'always' else
                  stdout.isatty())
    Out_Style.enable(enable_out)
    Out_Fore.enable(enable_out)

    enable_err = (False if color == 'never' else
                  True if color == 'always' else
                  stderr.isatty())
    Err_Style.enable(enable_err)
    Err_Fore.enable(enable_err)

def shorten_string(string, max_width):
    ''' make limited length string in form:
      "the string is very lo...(and 15 more)"
    '''
    string_len = len(string)
    if string_len <= max_width:
        return string
    visible = max_width - 16 - int(log10(string_len))
    # expected suffix len "...(and XXXXX more)"
    if not isinstance(string, unistr):
        visstring = unistr(string[:visible], errors='ignore')
    else:
        visstring = string[:visible]
    return u''.join((visstring, u'...(and ',
                     unistr(string_len - visible), u' more)'))


def get_console_width():
    try:
        cols = int(os.environ['COLUMNS'])
    except (KeyError, ValueError):
        pass
    else:
        if cols >= 25:
            return cols

    try:
        cols = max(25, int(os.popen('stty size', 'r').read().split()[1]))
    except Exception:
        pass
    else:
        return cols

    return 100

setup_color(True)
