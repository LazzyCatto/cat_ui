from cat_ui.containers import ContainerElement, BoxContainer, Alignment
from cat_ui.keyboard_manager import clear, get_key_raw, get_key_from_raw, Key, KeyType


class App():
    def __init__(self, width=100, height=50, main_window: ContainerElement=BoxContainer(alignment=Alignment.CENTER)):
        self.width = width
        self.height = height
        self.main_window = main_window
        self.running = False

    async def run(self):
        self.running = True
        clear()
        print(self.main_window.draw_on_screen(self.width, self.height), end="", flush=True)
        raw_key = get_key_raw()
        key, key_type = get_key_from_raw(raw_key)
        while True:
            if key_type == KeyType.COMBINATION and key[-1] == Key.C:
                break
            self.main_window.process_key(raw_key)
            if not self.running:
                break
            clear()
            print(self.main_window.draw_on_screen(self.width, self.height), end="", flush=True)
            raw_key = get_key_raw()
            key, key_type = get_key_from_raw(raw_key)

        clear()
        self.running = False
    
    def set_screen(self, window: ContainerElement):
        self.main_window = window
        self.main_window.select()
        if self.running:
            clear()
            print(self.main_window.draw_on_screen(self.width, self.height), end="", flush=True)
    
    def stop(self):
        self.running = False
