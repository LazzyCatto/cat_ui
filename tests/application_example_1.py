from cat_ui import Box, Alignment, App, Window
import asyncio

window = Window(Box(10, 5, alignment=Alignment.BOTTOM_RIGHT))
app = App(20, 10)
app.add_window(window)
asyncio.run(app.run())
