from cat_ui import Label, App, Window
import asyncio

app = App()
app.add_window(Window(Label("Hello world!")))
asyncio.run(app.run())
