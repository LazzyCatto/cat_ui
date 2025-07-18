from ui.containers import Alignment
from ui.visual import Label
from ui.keyboard_manager import get_key_from_raw, get_raw_from_key, Key, KeyType, printable


class InputField(Label):
    def __init__(self, text="", width=-1, max_length=-1, alignment=Alignment.TOP_LEFT, alowed_char=printable):
        super().__init__(text, width, alignment)
        self.alowed_char = alowed_char
        self.max_length = max_length
        self.selected = False
        self.selected_character = len(text)
        self.plane_text = text
        self.max_width = width
        self.actions = []

    def set_width(self, width):
        self.max_width = width
        self.update_label()
    
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
        if raw_key in self.alowed_char and (self.max_length == -1 or len(self.plane_text) < self.max_length):
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
        self.max_width = width
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
                super().set_text(f"\033[1m{self.plane_text[:self.selected_character]}\033[4m{self.plane_text[self.selected_character]}\033[0;0m\033[1m{self.plane_text[self.selected_character + 1:]}\033[0;0m", self.max_width)
            else:
                super().set_text(f"\033[1m{self.plane_text}_\033[0;0m", self.max_width)
        else:
            super().set_text(self.plane_text, self.max_width)
    
    def selectable(self):
        return True


class PasswordInput(Label):
    def __init__(self, text="", password_char="*", width=-1, max_length=-1, alignment=Alignment.TOP_LEFT, alowed_char=printable):
        super().__init__(text, width, alignment)
        self.alowed_char = alowed_char
        self.max_length = max_length
        self.password_char = password_char
        self.selected = False
        self.selected_character = len(text)
        self.plane_text = text
        self.max_width = width
        self.actions = []

    def set_width(self, width):
        self.max_width = width
        self.update_label()
    
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
        if raw_key in self.alowed_char and (self.max_length == -1 or len(self.plane_text) < self.max_length):
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
        self.max_width = width
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
                super().set_text(f"\033[1m{self.password_char * self.selected_character}\033[4m{self.password_char}\033[0;0m\033[1m{self.password_char * (len(self.plane_text) -  self.selected_character - 1)}\033[0;0m", self.max_width)
            else:
                super().set_text(f"\033[1m{self.password_char * len(self.plane_text)}_\033[0;0m", self.max_width)
        else:
            super().set_text(self.password_char * len(self.plane_text), self.max_width)
    
    def selectable(self):
        return True
