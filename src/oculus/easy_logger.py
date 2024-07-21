from enum import Enum

from colorama import Fore, Back, Style

from . import __short_name__, __long_name__, __version__
from .config import config

class LogLevel(Enum):
    FATAL = 0
    ERROR = 1
    WARNING = 2
    SUCCESS_ONLY = 3
    INFO = 4 # Default
    DEBUG = 5
    TRACE = 6

class NoColor:
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    LIGHTBLACK_EX = LIGHTRED_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTCYAN_EX = LIGHTWHITE_EX = ''
    DIM = NORMAL = BRIGHT = ''
    RESET = RESET_ALL = ''

_LINE_UP = '\033[1A'
_LINE_CLEAR = '\x1b[2L'

loglevel = int(config['General']['log_level'])

def overwrite_previous_line():
    print(_LINE_UP, end=_LINE_CLEAR)

def info(message:str):
    if loglevel < LogLevel.INFO.value:
        return
    print(f'{Fore.LIGHTCYAN_EX}{Style.BRIGHT}[*]{Style.RESET_ALL}{Fore.RESET} {message}')
