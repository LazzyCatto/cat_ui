from ui.containers import Alignment
from ui.visual import Label
from ui.keyboard_manager import get_key_from_raw, get_raw_from_key, Key, KeyType, printable


class InputField(Label):
    def __init__(self, text="", width=-1, alignment=Alignment.TOP_LEFT):
        super().__init__(text, width, alignment)
        self.selected = False
        self.selected_character = len(text)
        self.plane_text = text
        self.actions = []
    
    def select(self):
        self.selected = True
        self.update_label()
    
    def deselect(self):
        self.selected = False
        self.update_label()
    
    def process_key(self, raw_key):
        if raw_key in "\n\r":
            self.on_enter()
            return ""
        if raw_key in printable:
            self.plane_text = self.plane_text[:self.selected_character] + raw_key + self.plane_text[self.selected_character:]
            self.selected_character += 1
            self.update_label()
        key, key_type = get_key_from_raw(raw_key)
        key, key_type = get_key_from_raw(raw_key)
        if key_type == KeyType.COMBINATION:
            return get_raw_from_key(key[-1])
        if key_type == KeyType.ARROW:
            if key == Key.LEFT_ARROW:
                if self.selected_character > 0:
                    self.selected_character -= 1
                    self.update_label()
                    return ""
                return raw_key
            if key == Key.RIGHT_ARROW:
                if self.selected_character < len(self.plane_text):
                    self.selected_character += 1
                    self.update_label()
                    return ""
                return raw_key
        if key_type == KeyType.OTHER:
            if key == Key.BACKSPASE:
                if self.selected_character > 0:
                    self.plane_text = self.plane_text[:self.selected_character - 1] + self.plane_text[self.selected_character:]
                    self.selected_character -= 1
                    self.update_label()
        return raw_key
    
    def set_text(self, text, width=-1):
        self.plane_text = text
        self.update_label()
    
    def get_text(self):
        return self.plane_text

    def add_action(self, on_click):
        self.actions.append(on_click)

    def on_enter(self):
        for action in self.actions:
            action(self)

    def update_label(self):
        if self.selected:
            if self.selected_character < len(self.plane_text):
                super().set_text(f"\033[1m{self.plane_text[:self.selected_character]}\033[4m{self.plane_text[self.selected_character]}\033[0;0m\033[1m{self.plane_text[self.selected_character + 1:]}\033[0m")
            else:
                super().set_text(f"\033[1m{self.plane_text}_\033[0m")
        else:
            super().set_text(self.plane_text)
