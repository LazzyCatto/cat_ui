from cat_ui.keyboard_manager import move_left, move_right, move_up, move_down, get_key_from_raw, get_raw_from_key, Key, KeyType
from enum import Enum


class Alignment(Enum):
    TOP_LEFT = (0, 0)
    TOP_CENTER = (0, 0.5)
    TOP_RIGHT = (0, 1)
    CENTER_LEFT = (0.5, 0)
    CENTER = (0.5, 0.5)
    CENTER_RIGHT = (0.5, 1)
    BOTTOM_LEFT = (1, 0)
    BOTTOM_CENTER = (1, 0.5)
    BOTTOM_RIGHT = (1, 1)


class ContainerElement:
    def __init__(self, width, height, alignment: Alignment=Alignment.TOP_LEFT):
        self.width = width
        self.height = height
        self.alignment = alignment

    def draw(self):
        return ""

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def draw_on_screen(self, screen_width=0, screen_height=0):
        horizontal_alignment = "{context}"
        if int((screen_width - self.get_width())*self.alignment.value[1]) > 0:
            horizontal_alignment = f"\033[{int((screen_width - self.get_width())*self.alignment.value[1])}C{{context}}\033[{int((screen_width - self.get_width())*self.alignment.value[1])}D"
        vertical_alignment = "{context}"
        if int((screen_height - self.get_height())*self.alignment.value[0]) > 0:
            vertical_alignment = f"\033[{int((screen_height - self.get_height())*self.alignment.value[0])}B{{context}}\033[{int((screen_height - self.get_height())*self.alignment.value[0])}A"
        return vertical_alignment.format(context=horizontal_alignment.format(context=self.draw()))
    
    def process_key(self, raw_key):
        return raw_key
    
    def select(self):
        pass
    
    def deselect(self):
        pass

    def selectable(self):
        return False


class Box(ContainerElement):
    def __init__(self, width, height, alignment: Alignment=Alignment.TOP_LEFT, **style):
        super().__init__(width, height, alignment)
        self.set_style(**style)

    def set_style(self, vertical_bar="|", horizontal_bar="-", corners=["*", "*", "*", "*"], fill=" "):
        self.vertical_bar = vertical_bar
        self.horizonal_bar = horizontal_bar
        self.corners = corners
        self.fill = fill

    def draw(self):
        text = f"{self.vertical_bar}{self.fill*(self.get_width()-2)}{self.vertical_bar}{move_left(self.get_width())}\033[1B"*(self.get_height()-2)
        return f"\033[s{self.corners[0]}{self.horizonal_bar*(self.get_width() - 2)}{self.corners[1]}{move_left(self.get_width())}\033[1B{text}{self.corners[2]}{self.horizonal_bar*(self.get_width() - 2)}{self.corners[3]}\033[u"


class BoxContainer(Box):
    def __init__(self, min_width=3, min_height=3, left_padding=1, right_padding=1, top_padding=1, bottom_padding=1, alignment: Alignment=Alignment.TOP_LEFT, **style):
        super().__init__(min_width, min_height, alignment, **style)
        self.left_padding = left_padding
        self.right_padding = right_padding
        self.top_padding = top_padding
        self.bottom_padding = bottom_padding
        self.children: list[ContainerElement] = []
        self.selection_index = 0
    
    def append(self, child: ContainerElement):
        self.children.append(child)
    
    def get_width(self):
        return max(self.width, self.left_padding + self.right_padding + (max([child.get_width() for child in self.children]) if self.children else 0))
    
    def get_height(self):
        return max(self.height, self.top_padding + self.bottom_padding + (max([child.get_height() for child in self.children]) if self.children else 0))
    
    def draw(self):
        children_draw = "".join([child.draw_on_screen(self.get_width() - self.left_padding - self.right_padding, self.get_height() - self.top_padding - self.bottom_padding) for child in self.children])
        return f"{super().draw()}{move_right(self.left_padding)}{move_down(self.top_padding)}{children_draw}{move_up(self.left_padding)}{move_left(self.left_padding)}"
    
    def select(self):
        if not self.children[self.selection_index].selectable():
            self.selection_index = 0
            while not self.children[self.selection_index].selectable():
                self.selection_index += 1
                if self.selection_index == len(self.children):
                    return
        self.children[self.selection_index].select()
    
    def deselect(self):
        self.children[self.selection_index].deselect()
    
    def process_key(self, raw_key):
        if not self.children:
            return raw_key
        raw_key = self.children[self.selection_index].process_key(raw_key)
        key, key_type = get_key_from_raw(raw_key)
        if key_type == KeyType.COMBINATION:
            return get_raw_from_key(key[-1])
        if key_type == KeyType.ARROW:
            if key in [Key.UP_ARROW, Key.LEFT_ARROW]:
                new_selection = self.selection_index - 1
                found_selection = False
                while new_selection >= 0:
                    if self.children[new_selection].selectable():
                        found_selection = True
                        break
                    new_selection -= 1
                if found_selection:
                    self.children[self.selection_index].deselect()
                    self.selection_index = new_selection
                    self.children[self.selection_index].select()
                    return ""
                return raw_key
            new_selection = self.selection_index + 1
            found_selection = False
            while new_selection < len(self.children):
                if self.children[new_selection].selectable():
                    found_selection = True
                    break
                new_selection += 1
            if found_selection:
                self.children[self.selection_index].deselect()
                self.selection_index = new_selection
                self.children[self.selection_index].select()
                return ""
            return raw_key
        return raw_key
    
    def selectable(self):
        return any([child.selectable() for child in self.children])


class VerticalList(ContainerElement):
    def __init__(self, min_width=3, min_height=3, space=1, alignment: Alignment=Alignment.TOP_LEFT):
        super().__init__(min_width, min_height, alignment)
        self.space = space
        self.children: list[ContainerElement] = []
        self.selection_index = 0
    
    def append(self, child: ContainerElement):
        self.children.append(child)
    
    def get_width(self):
        return max(self.width, max([child.get_width() for child in self.children]) if self.children else 0)
    
    def get_height(self):
        return max(self.height, (sum([child.get_height() + self.space for child in self.children]) if self.children else 0) - self.space)
    
    def draw(self):
        total_movement = sum([child.get_height() + self.space for child in self.children]) - self.space
        children_draw = move_down(self.space).join([f"{child.draw_on_screen(screen_width=self.get_width())}{move_down(child.get_height())}" for child in self.children])
        return f"{children_draw}{move_up(total_movement)}"
    
    def select(self):
        if not self.children[self.selection_index].selectable():
            self.selection_index = 0
            while not self.children[self.selection_index].selectable():
                self.selection_index += 1
                if self.selection_index == len(self.children):
                    return
        self.children[self.selection_index].select()
    
    def deselect(self):
        self.children[self.selection_index].deselect()
    
    def process_key(self, raw_key):
        if not self.children:
            return raw_key
        raw_key = self.children[self.selection_index].process_key(raw_key)
        key, key_type = get_key_from_raw(raw_key)
        if key_type == KeyType.COMBINATION:
            return get_raw_from_key(key[-1])
        if key_type == KeyType.ARROW:
            if key == Key.UP_ARROW:
                new_selection = self.selection_index - 1
                found_selection = False
                while new_selection >= 0:
                    if self.children[new_selection].selectable():
                        found_selection = True
                        break
                    new_selection -= 1
                if found_selection:
                    self.children[self.selection_index].deselect()
                    self.selection_index = new_selection
                    self.children[self.selection_index].select()
                    return ""
                return raw_key
            if key == Key.DOWN_ARROW:
                new_selection = self.selection_index + 1
                found_selection = False
                while new_selection < len(self.children):
                    if self.children[new_selection].selectable():
                        found_selection = True
                        break
                    new_selection += 1
                if found_selection:
                    self.children[self.selection_index].deselect()
                    self.selection_index = new_selection
                    self.children[self.selection_index].select()
                    return ""
                return raw_key
        return raw_key
    
    def selectable(self):
        return any([child.selectable() for child in self.children])


class HorizontalList(ContainerElement):
    def __init__(self, min_width=3, min_height=3, space=1, alignment: Alignment=Alignment.TOP_LEFT):
        super().__init__(min_width, min_height, alignment)
        self.space = space
        self.children: list[ContainerElement] = []
        self.selection_index = 0
    
    def append(self, child: ContainerElement):
        self.children.append(child)
    
    def get_width(self):
        return max(self.width, (sum([child.get_width() + self.space for child in self.children]) if self.children else 0) - self.space)
    
    def get_height(self):
        return max(self.height, max([child.get_height() for child in self.children]) if self.children else 0)
    
    def draw(self):
        total_movement = sum([child.get_width() + self.space for child in self.children]) - self.space
        children_draw = move_right(self.space).join([f"{child.draw_on_screen(screen_height=self.get_height())}{move_right(child.get_width())}" for child in self.children])
        return f"{children_draw}{move_left(total_movement)}"
    
    def select(self):
        if not self.children[self.selection_index].selectable():
            self.selection_index = 0
            while not self.children[self.selection_index].selectable():
                self.selection_index += 1
                if self.selection_index == len(self.children):
                    return
        self.children[self.selection_index].select()
    
    def deselect(self):
        self.children[self.selection_index].deselect()
    
    def process_key(self, raw_key):
        if not self.children:
            return raw_key
        raw_key = self.children[self.selection_index].process_key(raw_key)
        key, key_type = get_key_from_raw(raw_key)
        if key_type == KeyType.COMBINATION:
            return get_raw_from_key(key[-1])
        if key_type == KeyType.ARROW:
            if key == Key.LEFT_ARROW:
                new_selection = self.selection_index - 1
                found_selection = False
                while new_selection >= 0:
                    if self.children[new_selection].selectable():
                        found_selection = True
                        break
                    new_selection -= 1
                if found_selection:
                    self.children[self.selection_index].deselect()
                    self.selection_index = new_selection
                    self.children[self.selection_index].select()
                    return ""
                return raw_key
            if key == Key.RIGHT_ARROW:
                new_selection = self.selection_index + 1
                found_selection = False
                while new_selection < len(self.children):
                    if self.children[new_selection].selectable():
                        found_selection = True
                        break
                    new_selection += 1
                if found_selection:
                    self.children[self.selection_index].deselect()
                    self.selection_index = new_selection
                    self.children[self.selection_index].select()
                    return ""
                return raw_key
        return raw_key
    
    def selectable(self):
        return any([child.selectable() for child in self.children])


class VerticalContainer(BoxContainer):
    def __init__(self, min_width=3, min_height=3, left_padding=1, right_padding=1, top_padding=1, bottom_padding=1, space=1, alignment = Alignment.TOP_LEFT, **style):
        super().__init__(min_width, min_height, left_padding, right_padding, top_padding, bottom_padding, alignment, **style)
        self.children = [VerticalList(min_width - left_padding - right_padding, min_height - top_padding - bottom_padding, space)]
    
    def append(self, child: ContainerElement):
        self.children[0].append(child)


class HorizontalContainer(BoxContainer):
    def __init__(self, min_width=3, min_height=3, left_padding=1, right_padding=1, top_padding=1, bottom_padding=1, space=1, alignment = Alignment.TOP_LEFT, **style):
        super().__init__(min_width, min_height, left_padding, right_padding, top_padding, bottom_padding, alignment, **style)
        self.children = [HorizontalList(min_width - left_padding - right_padding, min_height - top_padding - bottom_padding, space)]
    
    def append(self, child: ContainerElement):
        self.children[0].append(child)
