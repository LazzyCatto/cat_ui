import sys
import termios
import tty
import os
from enum import Enum
import string
import regex


ansi_pattern = regex.compile(r'(\x1B\[[0-?]*[ -/]*[@-~])')
printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'


class Key(Enum):
    LOWER_A = "a"
    LOWER_B = "b"
    LOWER_C = "c"
    LOWER_D = "d"
    LOWER_E = "e"
    LOWER_F = "f"
    LOWER_G = "g"
    LOWER_H = "h"
    LOWER_I = "i"
    LOWER_J = "j"
    LOWER_K = "k"
    LOWER_L = "l"
    LOWER_M = "m"
    LOWER_N = "n"
    LOWER_O = "o"
    LOWER_P = "p"
    LOWER_Q = "q"
    LOWER_R = "r"
    LOWER_S = "s"
    LOWER_T = "t"
    LOWER_U = "u"
    LOWER_V = "v"
    LOWER_W = "w"
    LOWER_X = "x"
    LOWER_Y = "y"
    LOWER_Z = "z"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4
    NUMBER_5 = 5
    NUMBER_6 = 6
    NUMBER_7 = 7
    NUMBER_8 = 8
    NUMBER_9 = 9
    UP_ARROW = "up"
    DOWN_ARROW = "down"
    RIGHT_ARROW = "right"
    LEFT_ARROW = "left"
    SHIFT = "shift"
    CTRL = "ctrl"
    ENTER = "enter"
    BACKSPASE = "backspace"
    OTHER = "other"


class KeyType(Enum):
    LETTER = 0
    NUMBER = 1
    ARROW = 2
    COMBINATION = 3
    OTHER = 4


def move_left(N):
    return f"\033[{N}D" if N > 0 else ""

def move_right(N):
    return f"\033[{N}C" if N > 0 else ""

def move_up(N):
    return f"\033[{N}A" if N > 0 else ""

def move_down(N):
    return f"\033[{N}B" if N > 0 else ""


def get_key_raw():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
            if ch == '\x1b[1':
                ch += sys.stdin.read(3)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def get_key_from_raw(key):
    key_to_arrow = {"A": Key.UP_ARROW, "B": Key.DOWN_ARROW, "C": Key.RIGHT_ARROW, "D": Key.LEFT_ARROW}
    key_to_special = {"2": Key.SHIFT, "5": Key.CTRL}

    if len(key) == 1:
        if key in string.ascii_letters:
            return Key(key), KeyType.LETTER
        if key in [str(num) for num in range(10)]:
            return Key(int(key)), KeyType.NUMBER
        if ord(key) == 13:
            return Key.ENTER, KeyType.OTHER
        if 1 <= ord(key) <= 26:
            return (Key.CTRL, Key(chr(ord(key) + 64))), KeyType.COMBINATION
        if key == "\x7f":
            return Key.BACKSPASE, KeyType.OTHER
        return Key.OTHER, KeyType.OTHER
    elif len(key) == 3:
        return key_to_arrow[key[-1]], KeyType.ARROW
    elif len(key) == 6:
        return (key_to_special[key[-2]], key_to_arrow[key[-1]]), KeyType.COMBINATION
    return Key.OTHER, KeyType.OTHER


def visible_length(s):
    clean = ansi_pattern.sub('', s)
    return len(clean)


def split_visible_chars(s):
        parts = []
        current_prefix = ''
        current_suffix = ''
        i = 0
        while i < len(s):
            match = ansi_pattern.match(s, i)
            if match:
                code = match.group(1)
                if code.endswith('m'):
                    if code == '\033[0m':
                        current_suffix += code
                    else:
                        current_prefix += code
                i = match.end()
            else:
                visible = s[i]
                fragment = current_prefix + visible + current_suffix
                parts.append(fragment)
                i += 1
                current_suffix = ''
        return parts


def get_raw_from_key(key: Key):
    if key == Key.UP_ARROW:
        return "\x1b[A"
    if key == Key.DOWN_ARROW:
        return "\x1b[B"
    if key == Key.RIGHT_ARROW:
        return "\x1b[C"
    if key == Key.LEFT_ARROW:
        return "\x1b[D"
    if key.value in string.ascii_letters:
        return key.value
    if key.value in range(10):
        return str(key.value)
    if key.value == Key.ENTER:
        return chr(13)
    raise KeyError()


def get_key():
    key = get_key_raw()
    return get_key_from_raw(key)


def clear():
    os.system('clear')
