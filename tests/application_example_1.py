from cat_ui import Box, Alignment, App
import asyncio

app = App(20, 10, Box(10, 5, alignment=Alignment.BOTTOM_RIGHT))
asyncio.run(app.run())
