from cat_ui import VerticalContainer, Button, Label, Alignment, App, Window
import asyncio

app = App()

window_1 = Window(VerticalContainer(alignment=Alignment.TOP_CENTER))
window_2 = Window(VerticalContainer(alignment=Alignment.TOP_CENTER))

def set_window(window):
    global app
    app.close_all_windows()
    app.add_window(window)

button = Button("next window", alignment=Alignment.BOTTOM_CENTER)
button.add_action(lambda btn: set_window(window_2))

window_1.context.append(Label("This is window 1"))
window_1.context.append(button)

window_2.context.append(Label("This is window 2"))

app.add_window(window_1)
asyncio.run(app.run())