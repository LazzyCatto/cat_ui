from cat_ui import Label, App
import asyncio

app = App(main_window=Label("Hello cat_ui!"))
asyncio.run(app.run())
