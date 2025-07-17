from ui.containers import BoxContainer, VerticalList, HorizontalList, Alignment
from ui.visual import Label
from ui.styles import pretty_style, bold_pretty_style


class Button(BoxContainer):
    def __init__(self, text: str="", min_width=3, min_height=3, left_padding=1, right_pading=1, top_pading=1, bottom_pading=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER, style=pretty_style, selected_style=bold_pretty_style):
        super().__init__(min_width, min_height, left_padding, right_pading, top_pading, bottom_pading, alignment, **style)
        self.children = [Label(text, alignment=text_alignment)]
        self.actions = []
        self.style = style
        self.selected_style = selected_style
    
    def append(self, child):
        raise NotImplementedError()
    
    def process_key(self, raw_key):
        if raw_key in "\n\r":
            self.on_click()
        return raw_key
    
    def select(self):
        self.set_style(**self.selected_style)
    
    def deselect(self):
        self.set_style(**self.style)
    
    def add_action(self, on_click):
        self.actions.append(on_click)

    def on_click(self):
        for action in self.actions:
            action(self)


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
        self.actions_on.append(on_click)
    
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
        return f"\033[s\033[1m{text}\033[0m\033[u" if self.selected else f"\033[s{text}\033[u"


class VerticalCheckbox(VerticalList):
    def __init__(self, options: list[str], min_width=3, min_height=3, space=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER_LEFT, chosen_prefix="*", plain_prefix=" "):
        super().__init__(min_width, min_height, space, alignment)
        self.children: list[SelectorLabel] = [SelectorLabel(option, chosen_prefix, plain_prefix, alignment=text_alignment) for option in options]
    
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

class HorizontalCheckbox(HorizontalList):
    def __init__(self, options: list[str], min_width=3, min_height=3, space=1, alignment=Alignment.TOP_LEFT, text_alignment=Alignment.CENTER_LEFT, chosen_prefix="*", plain_prefix=" "):
        super().__init__(min_width, min_height, space, alignment)
        self.children: list[SelectorLabel] = [SelectorLabel(option, chosen_prefix, plain_prefix, alignment=text_alignment) for option in options]
    
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