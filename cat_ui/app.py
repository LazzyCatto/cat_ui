from cat_ui.containers import ContainerElement, BoxContainer, Alignment
from cat_ui.keyboard_manager import clear, get_key_raw, get_key_from_raw, Key, KeyType


class Window:
    def __init__(self, context: ContainerElement=BoxContainer(alignment=Alignment.CENTER), layer=0):
        self.set_context(context)
        self.set_application()
        self.layer = layer
    
    def set_context(self, context: ContainerElement):
        self.context = context
        self.context.set_window(self)

    def select(self):
        self.context.select()
    
    def deselect(self):
        self.context.deselect()
    
    def process(self):
        raw_key = get_key_raw()
        key, key_type = get_key_from_raw(raw_key)
        if key_type == KeyType.COMBINATION and key[-1] == Key.C:
            self.close()
        self.context.process_key(raw_key)
    
    def set_application(self, app = None, window_id: int = -1):
        self.app = app
        self.id = window_id
    
    def update(self):
        if self.app:
            self.app.update()

    def draw(self):
        if self.app:
            self.draw_on_screen(self.app.width, self.app.height)
    
    def draw_on_screen(self, width, height):
        print(self.context.draw_on_screen(width, height), end="", flush=True)
    
    def close(self):
        if self.app:
            self.app.close_window(self.id)


class App:
    def __init__(self, width=100, height=50):
        self.width = width
        self.height = height
        self.windows: dict[int, Window] = {}
        self.current_window_id: int = -1
    
    def add_window(self, window: Window):
        window_id = id(window)
        self.windows[window_id] = window
        window.set_application(self, window_id)

        if self.current_window_id == -1:
            self.select_window(window_id)
    
        return window_id
    
    def open_window_on_top(self, window: Window):
        if self.windows:
            top_window = max(list(self.windows.values()), key=lambda x: x.layer)
            window.layer = top_window.layer + 1
        self.add_window(window)
        self.select_window(window.id)

    def close_window(self, window_id: int):
        self.windows[window_id].set_application()
        del self.windows[window_id]

        if self.current_window_id == window_id:
            self.select_first()
    
    def close_all_windows(self):
        for window in self.windows.values():
            window.set_application()
        self.windows.clear()
        self.current_window_id = -1
    
    def select_window(self, window_id):
        if self.current_window_id in self.windows:
            self.windows[self.current_window_id].deselect()
        if window_id not in self.windows:
            raise ValueError()
        self.current_window_id = window_id
        self.windows[window_id].select()
    
    def select_first(self):
        if not self.windows:
            self.current_window_id = -1
        else:
            self.select_window(max(list(self.windows.values()), key=lambda x: x.layer).id)

    def update(self):
        sorted_windows: list[Window] = list(self.windows.values())
        sorted_windows.sort(key=lambda window: window.layer)
        clear()
        for window in sorted_windows:
            window.draw()

    async def run(self):
        self.update()
        while self.windows and self.current_window_id != -1:
            self.windows[self.current_window_id].process()
            self.update()
        clear()
