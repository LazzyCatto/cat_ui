from cat_ui.containers import BoxContainer, VerticalList, HorizontalList, Alignment
from cat_ui.visual import Label
from cat_ui.styles import normal, bold_normal


class Button(BoxContainer):
    def __init__(self, text: str="", min_width=3, min_height=3, left_padding=1, right_padding=1, top_padding=1, bottom_padding=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER, style=normal, selected_style=bold_normal):
        super().__init__(min_width, min_height, left_padding, right_padding, top_padding, bottom_padding, alignment, **style)
        self.children: list[Label] = [Label(text, alignment=text_alignment)]
        self.actions = []
        self.style = style
        self.text = text
        self.selected_style = selected_style
    
    def append(self, child):
        raise NotImplementedError()
    
    def process_key(self, raw_key):
        if raw_key in "\n\r":
            self.on_click()
        return raw_key
    
    def set_text(self, text):
        self.text = text
        self.children[0].set_text(text)
    
    def get_text(self):
        return self.text

    def select(self):
        self.set_style(**self.selected_style)
        self.children[0].set_text(f"\033[1m{self.text}\033[0;0m")
    
    def deselect(self):
        self.set_style(**self.style)
        self.children[0].set_text(self.text)
    
    def add_action(self, on_click):
        self.actions.append(on_click)

    def on_click(self):
        for action in self.actions:
            action(self)
    
    def selectable(self):
        return True


class SelectorLabel(Label):
    def __init__(self, text, chosen_prefix="*", plain_prefix=" ", width=-1, alignment=Alignment.TOP_LEFT):
        super().__init__(plain_prefix + text, width, alignment)
        self.chosen_prefix = chosen_prefix
        self.plain_prefix = plain_prefix
        self.plain_text = text
        self.selected = False
        self.chosen = False
        self.actions_on = []
        self.actions_off = []

    def set_text(self, text: str, width = -1):
        self.plain_text = text
        self.width = len(self) if width == -1 else width
        self.height = (len(self) + width - 1) // width
    
    def select(self):
        self.selected = True
    
    def deselect(self):
        self.selected = False
    
    def add_action_on(self, on_click):
        self.actions_on.append(on_click)
        
    def add_action_off(self, on_click):
        self.actions_off.append(on_click)
    
    def chose(self, state: bool):
        self.chosen = state
        self.text = (self.chosen_prefix if state else self.plain_prefix) + self.plain_text
        self.height = (len(self) + self.width - 1) // self.width
        for action in self.actions_on if state else self.actions_off:
            action(self)
    
    def process_key(self, raw_key):
        if raw_key in '\n\r':
            self.chose(not self.chosen)
        return raw_key
    
    def draw(self):
        text = f"\033[1B\033[{self.width}D".join(self.get_splited())
        return f"\033[s\033[1m{text}\033[0;0m\033[u" if self.selected else f"\033[s{text}\033[u"
    
    def selectable(self):
        return True


class VerticalCheckbox(VerticalList):
    def __init__(self, options: list[str], min_width=3, min_height=3, space=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER_LEFT, chosen_prefix="*", plain_prefix=" "):
        super().__init__(min_width, min_height, space, alignment)
        self.children: list[SelectorLabel] = [SelectorLabel(option, chosen_prefix, plain_prefix, alignment=text_alignment) for option in options]
        self.actions = []
    
    def crop(self, max_width):
        for child in self.children:
            child.crop(max_width)

    def expand(self):
        for child in self.children:
            child.expand()
    
    def get_mask(self):
        return [child.chosen for child in self.children]
    
    def get_indices(self):
        indices = []
        for index, child in enumerate(self.children):
            if child.chosen:
                indices.append(index)
        return indices
    
    def process_key(self, raw_key):
        raw_key = super().process_key(raw_key)
        if raw_key in '\n\r':
            self.on_change()
        return raw_key
    
    def add_action(self, on_click):
        self.actions.append(on_click)

    def on_change(self):
        for action in self.actions:
            action(self)
    
    def selectable(self):
        return bool(self.children)

class HorizontalCheckbox(HorizontalList):
    def __init__(self, options: list[str], min_width=3, min_height=3, space=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER_LEFT, chosen_prefix="*", plain_prefix=" "):
        super().__init__(min_width, min_height, space, alignment)
        self.children: list[SelectorLabel] = [SelectorLabel(option, chosen_prefix, plain_prefix, alignment=text_alignment) for option in options]
        self.actions = []
    
    def crop(self, max_width):
        for child in self.children:
            child.crop(max_width)

    def expand(self):
        for child in self.children:
            child.expand()
    
    def get_mask(self):
        return [child.chosen for child in self.children]
    
    def get_indices(self):
        indices = []
        for index, child in enumerate(self.children):
            if child.chosen:
                indices.append(index)
        return indices
    
    def process_key(self, raw_key):
        raw_key = super().process_key(raw_key)
        if raw_key in '\n\r':
            self.on_change()
        return raw_key
    
    def add_action(self, on_click):
        self.actions.append(on_click)

    def on_change(self):
        for action in self.actions:
            action(self)
    
    def selectable(self):
        return bool(self.children)


class VerticalRadio(VerticalList):
    def __init__(self, options: list[str], min_width=3, min_height=3, space=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER_LEFT, chosen_prefix="*", plain_prefix=" "):
        super().__init__(min_width, min_height, space, alignment)
        self.children: list[SelectorLabel] = [SelectorLabel(option, chosen_prefix, plain_prefix, alignment=text_alignment) for option in options]
        def deselect_everyone_except(radio):
            for child in self.children:
                if child != radio:
                    child.chose(False)
        for child in self.children:
            child.add_action_on(deselect_everyone_except)
        self.actions = []
    
    def crop(self, max_width):
        for child in self.children:
            child.crop(max_width)

    def expand(self):
        for child in self.children:
            child.expand()
    
    def get_index(self):
        for index, child in enumerate(self.children):
            if child.chosen:
                return index
        return -1
    
    def process_key(self, raw_key):
        raw_key = super().process_key(raw_key)
        if raw_key in '\n\r':
            self.on_change()
        return raw_key
    
    def add_action(self, on_click):
        self.actions.append(on_click)

    def on_change(self):
        for action in self.actions:
            action(self)

    def selectable(self):
        return bool(self.children)

class HorizontalRadio(HorizontalList):
    def __init__(self, options: list[str], min_width=3, min_height=3, space=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER_LEFT, chosen_prefix="*", plain_prefix=" "):
        super().__init__(min_width, min_height, space, alignment)
        self.children: list[SelectorLabel] = [SelectorLabel(option, chosen_prefix, plain_prefix, alignment=text_alignment) for option in options]
        def deselect_everyone_except(radio):
            for child in self.children:
                if child != radio:
                    child.chose(False)
        for child in self.children:
            child.add_action_on(deselect_everyone_except)
        self.actions = []
    
    def crop(self, max_width):
        for child in self.children:
            child.crop(max_width)

    def expand(self):
        for child in self.children:
            child.expand()
    
    def get_index(self):
        for index, child in enumerate(self.children):
            if child.chosen:
                return index
        return -1
    
    def process_key(self, raw_key):
        raw_key = super().process_key(raw_key)
        if raw_key in '\n\r':
            self.on_change()
        return raw_key
    
    def add_action(self, on_click):
        self.actions.append(on_click)

    def on_change(self):
        for action in self.actions:
            action(self)

    def selectable(self):
        return bool(self.children)
