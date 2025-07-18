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
        blocks = self.text.split("\n")
        max_width = 0
        for block in blocks:
            max_width = max(visible_length(text) if width == -1 else width, max_width)
        self.width = max_width
        self.height = 0
        if self.width == 0:
            return
        for block in blocks:
            self.height += (visible_length(block) + self.width - 1) // self.width
    
    def get_text(self):
        return self.text

    def draw(self):
        text = f"\033[1B\033[{self.width}D".join(self.get_splited())
        return f"\033[s{text}\033[u"
    
    def get_splited(self):
        if self.width == 0:
            return []
        blocks = self.text.split("\n")
        splited = []
        for block in blocks:
            symbols = split_visible_chars(block)
            line_height = (visible_length(block) + self.width - 1) // self.width
            for line in range(line_height):
                line_content = "".join(symbols[self.get_width() * line: self.get_width() * (line + 1)])
                if visible_length(line_content) < self.get_width():
                    line_content += f"\033[{self.get_width() - visible_length(line_content)}C"
                splited.append(line_content)
        return splited
