from cat_ui import Label, run, set_screen
import asyncio

set_screen(Label("Hello cat_ui!"))
asyncio.run(run())
