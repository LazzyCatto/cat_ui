from cat_ui.containers import *
from cat_ui.keyboard_manager import *
from cat_ui.input_containers import *
from cat_ui.visual import *
from cat_ui.selectors import *
import cat_ui.styles as styles


SCREEN_WIDTH = 100
SCREEN_HEIGHT = 50

MAIN_WINDOW: ContainerElement = BoxContainer(alignment=Alignment.CENTER)


def set_screen(main_window: ContainerElement):
    global MAIN_WINDOW
    MAIN_WINDOW = main_window
    MAIN_WINDOW.select()


async def run():
    clear()
    print(MAIN_WINDOW.draw_on_screen(SCREEN_WIDTH, SCREEN_HEIGHT))
    raw_key = get_key_raw()
    key, key_type = get_key_from_raw(raw_key)
    while not (key_type == KeyType.COMBINATION and key[-1] == Key.C):
        MAIN_WINDOW.process_key(raw_key)
        clear()
        print(MAIN_WINDOW.draw_on_screen(SCREEN_WIDTH, SCREEN_HEIGHT))
        raw_key = get_key_raw()
        key, key_type = get_key_from_raw(raw_key)
    clear()


__all__ = [
    "styles",
    "ansi_pattern",
    "printable",
    "Key",
    "KeyType",
    "move_left",
    "move_right",
    "move_up",
    "move_down",
    "get_key_raw",
    "get_key_from_raw",
    "visible_length",
    "split_visible_chars",
    "get_raw_from_key",
    "get_key",
    "clear",
    "Alignment",
    "ContainerElement",
    "Box",
    "BoxContainer",
    "VerticalList",
    "HorizontalList",
    "VerticalContainer",
    "HorizontalContainer",
    "Button",
    "SelectorLabel",
    "VerticalCheckbox",
    "HorizontalCheckbox",
    "VerticalRadio",
    "HorizontalRadio",
    "Label",
    "InputField",
    "PasswordInput",
    "SCREEN_WIDTH",
    "SCREEN_HEIGHT",
    "run"
]
