from cat_ui import VerticalContainer, Label, Button, Alignment, App, Window
import asyncio

app = App(100, 20)

# main window
window = Window(VerticalContainer(min_width=40, min_height=10, left_padding=2,right_padding=2, alignment=Alignment.TOP_CENTER))

button_open = Button("click me", alignment=Alignment.CENTER)
button_open.add_action(lambda btn: app.open_window_on_top(popup))

window.context.append(Label("Open another window"))
window.context.append(button_open)

# popup
popup = Window(VerticalContainer(left_padding=2,right_padding=2, alignment=Alignment.CENTER))

button_close = Button("close", alignment=Alignment.CENTER)
button_close.add_action(lambda btn: btn.window.close())

popup.context.append(Label("This is new window"))
popup.context.append(button_close)

app.add_window(window)
asyncio.run(app.run())
