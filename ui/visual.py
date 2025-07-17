from ui.containers import ContainerElement, Alignment
from ui.keyboard_manager import visible_length, split_visible_chars


class Label(ContainerElement):
    def __init__(self, text: str, width = -1, alignment = Alignment.TOP_LEFT):
        width = len(text) if width == -1 else width
        super().__init__(width, (len(text) + width - 1) // width if width > 0 else 0, alignment)
        self.text = text
    
    def __len__(self):
        return visible_length(self.text)

    def crop(self, max_width):
        self.width = min(len(self), max_width)
        self.height = (len(self) + self.width - 1) // self.width

    def expand(self):
        self.width = len(self)
        self.height = 1
    
    def set_text(self, text: str, width = -1):
        self.text = text
        self.width = len(self) if width == -1 else width
        self.height = (len(self) + self.width - 1) // self.width if self.width > 0 else 0
    
    def get_text(self):
        return self.text

    def draw(self):
        text = f"\033[1B\033[{self.width}D".join(self.get_splited())
        return f"\033[s{text}\033[u"
    
    def get_splited(self):
        symbols = split_visible_chars(self.text)
        splited = []
        for line in range(self.get_height()):
            splited.append("".join(symbols[self.get_width() * line: self.get_width() * (line + 1)]))
        return splited
